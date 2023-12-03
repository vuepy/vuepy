<template>
<AppLayout :pane_widths="[0, 3, 1.5]" border="1px solid #cccccc" padding="10px">
<template v-slot:center>
<!--  编译-->
  <h2>编译llamacpp</h2>
  <Button description="Compile" @click="compile_llama_cpp()" button_style="info" width='100px'></Button>
  <hr></hr>

<!--  转换-->
  <h2>转换</h2>
  <Text v-model=hf_models_path.value :continuous_update="False" description="hf model" width="400px"></Text>
  <Button description="Convert" @click="convert_model()" button_style="info" width='100px'></Button>
  <hr></hr>

<!--  量化-->
  <h2>量化</h2>
  <HBox>
    <Dropdown :options="org_models.value" v-model="org_model.value" description="org model" width="500px"></Dropdown>
    <Dropdown :options="QUANTIZE_OPTS" v-model="quantize_opt.value" description="quantize" width="200px"></Dropdown>
  </HBox>
  <!-- todo 根据quantize_opt自动更新名字 -->
  <Text v-model=quantize_model.value :continuous_update="False" description="model out"></Text>
  <Button description="Quantize" @click="quantify_model()" button_style="info" width='100px'></Button>
  <hr></hr>

<!--  运行-->
  <h2>运行</h2>
  <HBox>
    <Dropdown :options="chat_models.value" v-model="chat.model" description="model" width="500px"></Dropdown>
    <Button icon="refresh" @click="refresh_models()" button_style="info" width='40px'></Button>
  </HBox>
  <Textarea v-model=chat.system description="SYS" width="500px"></Textarea>
  <Textarea v-model=chat.first_instruction description="first_instruction" width="500px"></Textarea>
  <FloatSlider v-model="chat.temp" description="temp" min=0 max=1 step=0.01 :continuous_update=False width="500px"></FloatSlider>
  <InputNumber v-model="chat.top_k" description="top_k" min=1 max=10000 step=1 :continuous_update=False width="500px"></InputNumber>
  <FloatSlider v-model="chat.top_p" description="top_p" min=0 max=1 step=0.01 :continuous_update=False width="500px"></FloatSlider>
  <FloatSlider v-model="chat.repeat_penalty" description="repeat_penalty" min=1 max=2 step=0.1 :continuous_update=False width="500px"></FloatSlider>
  <Button description="Run" @click="exec_chat()" button_style="info" width='60px'></Button>

</template>


</AppLayout>
</template>

<script setup>
import {ref, reactive} from 'vue';
import AppLayout from "../ipywidgets_vue/AppLayout";
import Button from "../ipywidgets_vue/Button";
import Dropdown from "../ipywidgets_vue/Dropdown";
import Text from "../ipywidgets_vue/Text";
import Textarea from "../ipywidgets_vue/Textarea";
import HBox from "../ipywidgets_vue/HBox";
import FloatSlider from "../ipywidgets_vue/FloatSlider";
import Slider from "../ipywidgets_vue/Slider";
import InputNumber from "../ipywidgets_vue/InputNumber";

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
  'ctx-size': 2048,  // size of the prompt context (default: 512, 0 = loaded from model)
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