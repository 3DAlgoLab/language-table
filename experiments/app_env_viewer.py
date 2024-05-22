# Check env.
import glob
import gradio as gr

from language_table.environments import blocks
from language_table.environments import language_table
from language_table.environments.rewards import block2block
import numpy as np
from icecream import ic

env = None
obs = None


def decode_inst(inst):
    """Utility to decode encoded language instruction"""
    return bytes(inst[np.where(inst != 0)].tolist()).decode("utf-8")


def init():
    """Initialize the environment"""
    global env, obs

    if env is not None:
        env.close()
        del env

    if obs is not None:
        del obs

    reward_factory = (
        block2block.BlockToBlockReward
    )  # CHANGE ME: change to another reward.
    env = language_table.LanguageTable(
        block_mode=blocks.LanguageTableBlockVariants.BLOCK_8,
        reward_factory=reward_factory,
        seed=0,
    )
    obs = env.reset()
    print("Environment initialized.")
    return get_current_observation()


def get_current_observation():
    if obs is not None:
        return obs["rgb"]
    return None


def get_current_instruction():
    if obs is not None:
        return decode_inst(obs["instruction"])
    return "No Instruction!"


def random_step():
    global obs
    if env is not None:
        action = env.action_space.sample()
        ic(action)
        obs, reward, done, info = env.step(action)
        return get_current_observation()
    return None


with gr.Blocks(title="Robot Env. Viewer") as demo:
    gr.Markdown("## Environment Viewer")
    gr.Textbox(value=get_current_instruction, label="Instruction", interactive=False)
    img = gr.Image(
        label="observation",
        interactive=False,
        value=get_current_observation,  # type: ignore
    )
    with gr.Row():
        btn_reset = gr.Button("Reset")
        btn_reset.click(init, inputs=None, outputs=img)
        btn_step = gr.Button("Random Step")
        btn_step.click(random_step, inputs=None, outputs=img)


if __name__ == "__main__":
    init()
    demo.launch()
