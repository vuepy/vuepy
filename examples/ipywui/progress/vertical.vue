
<template>
  <HBox>
    <Progress label="Default" vertical
              :value="80" :min="1" :max="100"></Progress>

    <Progress label="Info" type="info" vertical
              :value="60" :min="1" :max="100"></Progress>

    <Progress label="Success" type="success" vertical
              :value="50" :min="1" :max="100"></Progress>

    <Progress label="Warning" type="warning" vertical
              :value="40" :min="1" :max="100"></Progress>

    <Progress label="Danger" type="danger" vertical
              :value="30" :min="1" :max="100"></Progress>
  </HBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Progress from "../../../src/ipywui/components/Progress";
import HBox from "../../../src/ipywui/components/HBox";
</script>