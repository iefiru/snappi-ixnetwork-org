import pytest


def test_flow_sizes(api, settings):
    """
    This will test supported Flow Size
            'float': 'fixed',
            'int': 'fixed',
            'SizeIncrement': 'increment',
            'SizeRandom': 'random',
    """
    config = api.config()

    tx, rx = (
        config.ports
        .port(name='tx', location=settings.ports[0])
        .port(name='rx', location=settings.ports[1])
    )

    l1 = config.layer1.layer1()[0]
    l1.name = 'l1'
    l1.port_names = [rx.name, tx.name]
    l1.media = settings.media

    fixed_size, increment_size, random_size = (
        config.flows
        .flow(name='Fixed Size')
        .flow(name='Increment Size')
        .flow(name='Random Size')
    )

    fixed_size.tx_rx.port.tx_name = tx.name
    fixed_size.tx_rx.port.rx_name = rx.name
    pfc, = fixed_size.packet.pfcpause()
    pfc.src.value = '00:AB:BC:AB:BC:AB'
    pfc.dst.value = '00:AB:BC:AB:BC:AB'
    pfc.ether_type.value = '8100'
    pfc.class_enable_vector.value = 'FF'
    pfc.control_op_code.value = '0101'
    pfc.pause_class_0.value = 'FFFF'
    pfc.pause_class_1.value = 'FFFF'
    pfc.pause_class_2.value = 'FFFF'
    pfc.pause_class_3.value = 'FFFF'
    pfc.pause_class_4.value = 'FFFF'
    pfc.pause_class_5.value = 'FFFF'
    pfc.pause_class_6.value = 'FFFF'
    pfc.pause_class_7.value = 'FFFF'
    fixed_size.size.fixed = "44"

    increment_size.tx_rx.port.tx_name = tx.name
    increment_size.tx_rx.port.rx_name = rx.name
    increment_size.size.increment.start = "100"
    increment_size.size.increment.step = "10"
    increment_size.size.increment.end = "1200"

    random_size.tx_rx.port.tx_name = tx.name
    random_size.tx_rx.port.rx_name = rx.name
    random_size.size.random.min = "72"
    random_size.size.random.max = "1518"

    response = api.set_config(config)
    assert(len(response.errors)) == 0


if __name__ == '__main__':
    pytest.main(['-s', __file__])
