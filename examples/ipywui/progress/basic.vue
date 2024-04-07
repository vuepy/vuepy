<template>
  <VBox>
    <Progress label="Default"
              :value="80" :min="1" :max="100"></Progress>

    <Progress label="Info" type="info"
              :value="60" :min="1" :max="100"></Progress>

    <Progress label="Success" type="success"
              :value="50" :min="1" :max="100"></Progress>

    <Progress label="Warning" type="warning"
              :value="40" :min="1" :max="100"></Progress>

    <Progress label="Danger" type="danger"
              :value="30" :min="1" :max="100"></Progress>
  </VBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Progress from "../../../src/ipywui/components/Progress";
import VBox from "../../../src/ipywui/components/VBox";
</script>