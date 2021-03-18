from window import jobs_window, data_window, start_window


def test_start_window(qtbot):
    window = start_window()
    qtbot.addWidget(window)
    window.show()
    assert window.isVisible()


def test_jobs_window(qtbot):
    window = jobs_window()
    qtbot.addWidget(window)
    window.show()
    assert window.isVisible()


def test_data_window(qtbot):
    window = data_window()
    qtbot.addWidget(window)
    window.show()
    assert window.isVisible()
