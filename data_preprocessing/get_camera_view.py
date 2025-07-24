import argparse
import json

import robosuite
from robosuite import load_controller_config
from robosuite.wrappers import VisualizationWrapper
from termcolor import colored

from robocasa.scripts.collect_demos import collect_human_trajectory

def main(task=None, layout=10, style=3, device="keyboard", renderer="default_renderer"):    # Arguments
    if task is None:
        parser = argparse.ArgumentParser()
        parser.add_argument("--task", type=str, help="task (choose among 100+ tasks)")
        parser.add_argument("--layout", type=int, default=1, help="kitchen layout (choose number 0-9)")
        parser.add_argument("--style", type=int, default=10, help="kitchen style (choose number 0-11)")
        parser.add_argument(
            "--device", type=str, default="keyboard", choices=["keyboard", "spacemouse"]
        )
        parser.add_argument('--renderer', type=str, default='default_renderer', help='Renderer type')
    
        args = parser.parse_args()

    config = {
        "env_name": "PnPCounterToCab",
        "robots": "PandaMobile",
        "controller_configs": load_controller_config(default_controller="OSC_POSE"),
        "layout_ids": args.layout,
        "style_ids": args.style,
        "translucent_robot": True,
    }

    print(colored(f"Initializing environment...", "yellow"))
    env = robosuite.make(
        **config,
        has_renderer=True,
        has_offscreen_renderer=True,
        render_camera="robot0_frontview",
        ignore_done=True,
        use_camera_obs=True,
        control_freq=20,
        camera_depths=True,
        camera_names=["robot0_frontview", "birdview"], 
        renderer="mjviewer",
        render_collision_mesh=False,
        render_visual_mesh=False,
    )

    env = VisualizationWrapper(env)
    env_info = json.dumps(config)

    if args.device == "keyboard":
        from robosuite.devices import Keyboard

        device = Keyboard(env=env, pos_sensitivity=4.0, rot_sensitivity=4.0)
    elif args.device == "spacemouse":
        from robosuite.devices import SpaceMouse

        device = SpaceMouse(
            env=env,
            pos_sensitivity=4.0,
            rot_sensitivity=4.0,
        )
    else:
        raise ValueError
    
    # collect demonstrations
    while True:
        ep_directory, discard_traj = collect_human_trajectory(
            env,
            device,
            "right",
            "single-arm-opposed",
            mirror_actions=True,
            render=(args.renderer != "mjviewer"),
            max_fr=30,
            capture_images=True,
        )
        print()

if __name__ == "__main__":
    main()