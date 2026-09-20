"""Verify independent connection cells using mock accounts, never real credentials."""
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
nb = json.loads((ROOT / 'OpenQARP_Research_06_MultiProvider_MaxCut_Colab.ipynb').read_text(encoding='utf-8'))
cells = [''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code']


def source(prefix):
    return next(c for c in cells if c.startswith(prefix))


setup = source('# Shared hardware setup')
ibm = source('# IBM connection')
iqm = source('# IQM Qrisp connection')
bridge = source('# IQM benchmark adapter')
smoke = source('# Optional Qrisp hardware measurement')
scope = dict(os=SimpleNamespace(environ={}), Path=Path, SHOTS=64,
             SAMPLE_SEEDS=[1, 2], EXPERIMENT_ID='offline', N=5, THETA=[0.1, 0.2],
             qiskit_circuit=lambda *args: 'source-circuit',
             compile_for_backend=lambda circuit, backend, **kwargs: 'compiled-' + backend.name)
exec(setup, scope)

backend = SimpleNamespace(name='ibm_test', num_qubits=5, configuration=lambda: SimpleNamespace(simulator=False))
service = MagicMock()
service.backends.return_value = [backend]
service.backend.return_value = backend
ibm_class = MagicMock(return_value=service)
qr_backend = MagicMock()
qr_class = MagicMock(return_value=qr_backend)
iqm_backend = SimpleNamespace(name='garnet', num_qubits=20, operation_names=['r', 'cz', 'measure'])
provider = MagicMock()
provider.get_backend.return_value = iqm_backend
provider_class = MagicMock(return_value=provider)

with patch('qiskit_ibm_runtime.QiskitRuntimeService', ibm_class), \
     patch('qrisp.interface.IQMBackend', qr_class), \
     patch('iqm.qiskit_iqm.IQMProvider', provider_class):
    # Default Run All neither creates accounts nor accesses either provider.
    exec(ibm, scope); exec(iqm, scope); exec(bridge, scope); exec(smoke, scope)
    ibm_class.assert_not_called(); qr_class.assert_not_called(); provider_class.assert_not_called()

    for pair in [('IBM_TOKEN', 'IBM_CRN'), ('IBM_QUANTUM_TOKEN', 'IBM_QUANTUM_CRN')]:
        scope['os'].environ = {pair[0]: 'offline-token', pair[1]: 'offline-crn'}
        enabled_ibm = ibm.replace('CONNECT_IBM = False', 'CONNECT_IBM = True')
        exec(enabled_ibm, scope)
        assert ibm_class.call_args.kwargs == dict(channel='ibm_quantum_platform', token='offline-token', instance='offline-crn')
        assert 'IBM' not in scope['HARDWARE'], 'Account validation must not select a backend'
        exec(enabled_ibm.replace('IBM_BACKEND = ""', 'IBM_BACKEND = "ibm_test"'), scope)
        assert scope['HARDWARE']['IBM']['backend'] is backend
    ibm_class.save_account.assert_not_called()

    # Save-account behavior is explicit and uses the correct instance keyword.
    exec(enabled_ibm.replace('SAVE_IBM_ACCOUNT = False', 'SAVE_IBM_ACCOUNT = True'), scope)
    assert ibm_class.save_account.call_args.kwargs['instance'] == 'offline-crn'
    assert ibm_class.save_account.call_args.kwargs['name'] == 'ibm_qgss2025_dkt_ca'

    # A partial preferred pair must not borrow the CRN from another account.
    scope['os'].environ = {'IBM_TOKEN': 'offline-token', 'IBM_QUANTUM_CRN': 'other-crn'}
    try:
        scope['ibm_credentials']()
    except ValueError as error:
        assert 'both IBM_TOKEN and IBM_CRN' in str(error)
    else:
        raise AssertionError('Mixed IBM credential pairs were accepted')

    # IQM works with only its own token, and preserves prepared IBM state.
    scope['os'].environ = {'IQM_API_TOKEN': 'offline-iqm-token'}
    scope['HARDWARE']['IBM'] = {'backend': backend, 'circuit': 'ibm-circuit'}
    exec(iqm.replace('CONNECT_IQM = False', 'CONNECT_IQM = True'), scope)
    assert scope['quantum_computer'] is qr_backend
    assert qr_class.call_args.kwargs == dict(token='offline-iqm-token', device_instance='garnet', server_url='https://resonance.iqm.tech/')
    assert 'IBM' in scope['HARDWARE']
    exec(bridge, scope)
    assert set(scope['HARDWARE']) == {'IBM', 'IQM'}
    assert scope['HARDWARE']['IQM']['backend'] is iqm_backend
    assert scope['quantum_computer'] is not scope['HARDWARE']['IQM']['backend']

    # Sirius can connect through Qrisp without being treated as a validated benchmark target.
    exec(iqm.replace('CONNECT_IQM = False', 'CONNECT_IQM = True').replace('IQM_DEVICE = "garnet"', 'IQM_DEVICE = "sirius"'), scope)
    assert qr_class.call_args.kwargs['device_instance'] == 'sirius'
    iqm_backend.operation_names = ['r', 'cz', 'move', 'measure']
    exec(bridge, scope)
    assert 'IQM' not in scope['HARDWARE'] and 'IBM' in scope['HARDWARE']

    # The separate + state demonstration uses the Qrisp adapter and explicit shots.
    plus = MagicMock()
    plus.get_measurement.return_value = {'0': 0.5, '1': 0.5}
    scope.update(QuantumVariable=MagicMock(return_value=plus), qr_h=MagicMock())
    exec(smoke.replace('RUN_IQM_QRISP_SMOKE_TEST = False', 'RUN_IQM_QRISP_SMOKE_TEST = True'), scope)
    plus.get_measurement.assert_called_once_with(backend=qr_backend, shots=128)

print('PASS: independent provider cells, both IBM credential pairs, correct instance keyword, explicit saving, IQM adapter separation, and optional Qrisp measurement.')
