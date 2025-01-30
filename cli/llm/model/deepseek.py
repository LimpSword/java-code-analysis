# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Callable

from llm_core.assistants.base import BaseAssistant
from llm_core.llm.base import LLMBase
from llm_core.parsers import BaseParser
from openai import OpenAI

from decouple import config


def load_openai_client(llm, **kwargs):
    client_kwargs = {}
    client_kwargs.update(kwargs)

    api_key = client_kwargs.pop("api_key", config("OPENAI_API_KEY", default=None))

    client = OpenAI(base_url="https://api.deepseek.com", api_key=api_key, **kwargs)
    return client


def create_openai_completion(
        llm,
        model,
        messages,
        temperature,
        tools=None,
        tool_choice=None,
        schema=None,
):
    additional_kwargs = {}

    if tools and "gpt-4o" in model:
        additional_kwargs.update({"parallel_tool_calls": False})

    completion = llm._client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        tools=tools,
        tool_choice=tool_choice,
        **additional_kwargs,
    )
    return completion.dict()


@dataclass
class DeepSeekChatModel(LLMBase):
    create_completion: Callable = create_openai_completion
    loader: Callable = load_openai_client
    loader_kwargs: dict = None

    def __enter__(self):
        self.load_model()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release_model()

    def load_model(self):
        kwargs = self.loader_kwargs or {}
        self._client = self.loader(llm=self, **kwargs)

    def release_model(self):
        del self._client

    @property
    def ctx_size(self):
        ctx_size_map = {
            "deepseek-chat": 64_000,
            "deepseek-reasoner": 64_000,
        }

        if self.name in ctx_size_map:
            return ctx_size_map[self.name]
        else:
            #: we don't know the model, so we'll default
            #: to a large context window of 128k tokens
            return 128_000



@dataclass
class DeepSeekParser(BaseParser):
    target_cls: Callable
    model: str = "deepseek-chat"
    model_cls: Callable = DeepSeekChatModel

@dataclass
class DeepSeekAssistant(BaseAssistant, DeepSeekParser):
    model: str = "deepseek-chat"
    model_cls: Callable = DeepSeekChatModel