<template>
  <FileUpload v-model="files.value" accept=".txt"></FileUpload>
  <Input label="file info"
         :value="upload_file.value"
         type="textarea"
         style="height: 200px"
  ></Input>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import FileUpload from "../../../src/ipywui/components/FileUpload";
import Input from "../../../src/ipywui/components/Input";
</script>