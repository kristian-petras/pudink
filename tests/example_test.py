from pudink.client.frontend.scene_manager import SceneManager


def test_example():
    assert 1 + 1 == 2


def test_when_scene_is_switched_to_then_it_is_current_scene(mocker):
    # given
    window = mocker.patch("pyglet.window.Window")
    base_renderer = mocker.patch("pudink.client.renderer.base_renderer.BaseRenderer")
    sm = SceneManager(window)

    sm.register_scene("initial", base_renderer)

    # when
    sm.switch_to_scene("initial")

    # then
    assert sm.current_scene == base_renderer
