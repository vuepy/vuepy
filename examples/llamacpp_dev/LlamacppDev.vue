<template>
  <AppLayout :pane_widths="[0, 3, 1.5]" border="1px solid #cccccc" padding="10px">
    <template v-slot:center>
      <Accordion>
        <AccordionItem title="编译llamacpp">
          <Button description="Compile" @click="compile_llama_cpp()" button_style="info" width='100px'></Button>
        </AccordionItem>

        <AccordionItem title="转换">
          <Text description="hf model"
                v-model=hf_models_path.value width="400px"></Text>
          <Button description="Convert" @click="convert_model()" button_style="info" width='100px'></Button>
        </AccordionItem>

        <AccordionItem title="量化">
          <HBox>
            <Dropdown
                description="Org model"
                :options="org_models.value" v-model="org_model.value"
                width="500px"
            ></Dropdown>
            <Dropdown
                description="Quantize"
                :options="QUANTIZE_OPTS" v-model="quantize_opt.value"
                width="200px"
            ></Dropdown>
          </HBox>
          <Text
              description="Model out"
              v-model=quantize_model.value
              width="500px"
          ></Text>
          <Button description="Quantize" @click="quantify_model()" button_style="info" width='100px'></Button>
        </AccordionItem>

        <AccordionItem title="运行">
          <HBox>
            <Dropdown
                description="Model"
                :options="chat_models.value" v-model="chat.model" width="500px"
            ></Dropdown>
            <Button icon="refresh" @click="refresh_models()" button_style="info" width='40px'></Button>
          </HBox>
          <Textarea
              description="SYSTEM"
              v-model=chat.system width="500px"
          ></Textarea>
          <Textarea
              description="1st_instruction"
              v-model=chat.first_instruction width="500px"
          ></Textarea>
          <InputNumber
              description="Max ctx size"
              v-model="chat.ctx_size" min=1 max=4096 step=1
              width="200px"
          ></InputNumber>
          <Slider
              description="Temperature"
              v-model="chat.temp" min=0 max=1 step=0.01
              width="300px"
          ></Slider>
          <InputNumber
              description="Top K"
              v-model="chat.top_k" min=1 max=10000 step=1
              width="200px"
          ></InputNumber>
          <Slider
              description="Top P"
              v-model="chat.top_p" min=0 max=1 step=0.01
              width="300px"
              tooltip=""
          ></Slider>
          <Slider
              description="Repeat penalty"
              v-model="chat.repeat_penalty" min=1 max=2 step=0.1
              width="300px"
          ></Slider>
          <Button description="Run" @click="exec_chat()" button_style="info" width='60px'></Button>
        </AccordionItem>
      </Accordion>
    </template> <!-- ./center -->
  </AppLayout>
</template>

<script src="./app.py"></script>
<script setup>
import {ref, reactive} from 'vue';
import AppLayout from "../../src/ipywui/components/AppLayout";
import Button from "../../src/ipywui/components/Button";
import Dropdown from "../../src/ipywui/components/Dropdown";
import Text from "../../src/ipywui/components/Text";
import Textarea from "../../src/ipywui/components/Textarea";
import HBox from "../../src/ipywui/components/HBox";
import Slider from "../../src/ipywui/components/Slider";
import InputNumber from "../../src/ipywui/components/InputNumber";
import Accordion from "../../src/ipywui/components/Accordion";
import AccordionItem from "../../src/ipywui/components/AccordionItem";

QUANTIZE_OPTS = ['q4_0', 'q4_1', 'q4_k', 'q5_0', 'q5_1', 'q5_k', 'q6_k', 'q8_0']
hf_models_path = ref('')
org_models = ref(get_gguf_models(hf_models_path.value))
org_model = ref('')
quantize_model = ref('')
quantize_opt = ref('q4_0')

chat_models = ref([])
chat = reactive({
  'model': null,
  'system': 'You are a helpful assistant. 你是一个乐于助人的助手。',
  'first_instruction': '',
  'ctx_size': 2048,  // size of the prompt context (default: 512, 0 = loaded from model)
  'threads': 8,
  'temp': 0.1,    // temperature (default: 0.8
  'top_k': 1000,  // top-k sampling (default: 40, 0=disabled
  'top_p': 0.99,  // top-p sampling (default: 0.9, 1.0=disabled
  'repeat_penalty': 2.0, // penalize repeat sequence of tokens (default: 1.1, 1.0 = disabled)
})

compile_llama_cpp = () => {}
convert_model = () => {}
quantify_model = () => {}
refresh_models = () => {}
exec_chat = () => {}

</script>