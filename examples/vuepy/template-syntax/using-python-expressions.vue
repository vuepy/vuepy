<template>
  <pre>
    number({{ number.value }}) + 1 = {{ number.value + 1 }}
    {{ 'YES' if ok.value else 'No'}}
    {{ '-'.join(message.value.split()) }}
    {{ type(1) }}
    {{ eval("1") }}
  </pre>
  <!-- 注意：原生html tag不支持该语法 -->
  <Input :value="f'list-{did.value}'">
    div
  </Input>
  <a :href="message.value">href</a>

  <Button @click="increment" :label="f'count is {count.value}'"></Button>
</template>

<script setup>
import Input from "../../../src/ipywui/components/Input";
import Button from "../../../src/ipywui/components/Button";
</script>

<script lang="py">
from vuepy import ref

number = ref(11)
ok = ref(True)
message = ref("hello world")
did = ref(11)

count = ref(0)
def increment(own):
    print(own)
    count.value += 1
</script>
