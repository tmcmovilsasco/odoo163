# -*- coding: utf-8 -*-

import requests,json
import openai
from odoo import api, fields, models, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class AiRobot(models.Model):
    _name = 'ai.robot'
    _description = 'Gpt Robot'
    _order = 'sequence, name'

    name = fields.Char(string='Name', translate=True, required=True)
    provider = fields.Selection(string="AI Provider", selection=[('openai', 'OpenAI'), ('azure', 'Azure')], required=True, default='openai')
    ai_model = fields.Selection(string="AI Model", selection=[
        ('gpt-4', 'Chatgpt 4'),
        ('gpt-3.5-turbo', 'Chatgpt 3.5 Turbo'),
        ('gpt-3.5-turbo-0301', 'Chatgpt 3.5 Turbo on 20230301'),
        ('text-davinci-003', 'Chatgpt 3 Davinci'),
        ('code-davinci-002', 'Chatgpt 2 Code Optimized'),
        ('text-davinci-002', 'Chatgpt 2 Davinci'),
        ('dall-e2', 'Dall-E Image'),
    ], required=True, default='gpt-3.5-turbo',
                             help="""
GPT-4: Can understand Image, generate natural language or code.
GPT-3.5: A set of models that improve on GPT-3 and can understand as well as generate natural language or code
DALL·E: A model that can generate and edit images given a natural language prompt
Whisper: A model that can convert audio into text
Embeddings:	A set of models that can convert text into a numerical form
CodexLimited: A set of models that can understand and generate code, including translating natural language to code
Moderation: A fine-tuned model that can detect whether text may be sensitive or unsafe
GPT-3	A set of models that can understand and generate natural language
                             """)
    openapi_api_key = fields.Char(string="API Key", help="Provide the API key here")
    temperature = fields.Float(string='Temperature', default=0.9)
    max_length = fields.Integer('Max Length', default=300)
    endpoint = fields.Char('End Point', default='https://api.openai.com/v1/chat/completions')
    engine = fields.Char('Engine', help='If use Azure, Please input the Model deployment name.')
    api_version = fields.Char('API Version', default='2022-12-01')
    sequence = fields.Integer('Sequence', help="Determine the display order", default=10)

    def action_disconnect(self):
        requests.delete('https://chatgpt.com/v1/disconnect')
        
    def get_ai(self, data, partner_name='odoo', *args):
        #     通用方法
        self.ensure_one()
        if hasattr(self, 'get_%s' % self.provider):
            return getattr(self, 'get_%s' % self.provider)(data, partner_name, *args)
        else:
            return _('No robot provider found')

    def get_openai(self, data, partner_name='odoo', *args):
        self.ensure_one()
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.openapi_api_key}"}
        R_TIMEOUT = 300
        o_url = self.endpoint or "https://api.openai.com/v1/chat/completions"
    
        # 以下处理 open ai
        #     获取模型信息
        # list_model = requests.get("https://api.openai.com/v1/models", headers=headers)
        # model_info = requests.get("https://api.openai.com/v1/models/%s" % ai_model, headers=headers)
        if self.ai_model == 'dall-e2':
            # todo: 处理 图像引擎，主要是返回参数到聊天中
            # image_url = response['data'][0]['url']
            # https://platform.openai.com/docs/guides/images/introduction
            pdata = {
                "prompt": data,
                "n": 3,
                "size": "1024x1024",
            }
            return '建设中'
        elif self.ai_model in ['gpt-3.5-turbo', 'gpt-3.5-turbo-0301']:
            pdata = {
                "model": self.ai_model,
                "messages": [{"role": "user", "content": data}],
                "temperature": 0.9,
                "max_tokens": self.max_length or 1000,
                "top_p": 1,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.6,
                "user": partner_name,
                "stop": ["Human:", "AI:"]
            }
            _logger.warning('=====================open input pdata: %s' % pdata)
            response = requests.post(o_url, data=json.dumps(pdata), headers=headers, timeout=R_TIMEOUT)
            res = response.json()
            if 'choices' in res:
                # for rec in res:
                #     res = rec['message']['content']
                res = '\n'.join([x['message']['content'] for x in res['choices']])
                return res
        else:
            pdata = {
                "model": self.ai_model,
                "prompt": data,
                "temperature": 0.9,
                "max_tokens": self.max_length or 1000,
                "top_p": 1,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.6,
                "user": partner_name,
                "stop": ["Human:", "AI:"]
            }
            response = requests.post(o_url, data=json.dumps(pdata), headers=headers, timeout=R_TIMEOUT)
            res = response.json()
            if 'choices' in res:
                res = '\n'.join([x['text'] for x in res['choices']])
                return res
    
        return "获取结果超时，请重新跟我聊聊。"

    def get_azure(self, data, partner_name='odoo', *args):
        self.ensure_one()
        # only for azure
        openai.api_type = self.provider
        if not self.endpoint:
            raise UserError(_("Please Set your AI robot's endpoint first."))
        openai.api_base = self.endpoint
        if not self.api_version:
            raise UserError(_("Please Set your AI robot's API Version first."))
        openai.api_version = self.api_version
        openai.api_key = self.openapi_api_key
        response = openai.Completion.create(
            engine=self.engine,
            prompt=data,
            temperature=self.temperature or 0.9,
            max_tokens=self.max_length or 600,
            top_p=0.5,
            frequency_penalty=0,
            presence_penalty=0, stop=["Human:", "AI:"])

        _logger.warning('=====================azure input data: %s' % data)
        if 'choices' in response:
            res = response['choices'][0]['text'].replace(' .', '.').strip()
            return res

    @api.onchange('provider')
    def _onchange_provider(self):
        if self.provider == 'openai':
            self.endpoint = 'https://api.openai.com/v1/chat/completions'
        elif self.provider == 'azure':
            self.endpoint = 'https://odoo.openai.azure.com'
            
