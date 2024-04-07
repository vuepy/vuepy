<template>
  <Row align="flex-start">
    <Col :span="5">
      <Button label="" style="width: auto; background-color: #9dacc1"></Button>
    </Col>
  </Row>

  <Row justify="flex-end">
    <Col :span="5">
      <Button label="" style="width: auto; background-color: #9dacc1"></Button>
    </Col>
    <Col :span="5">
      <Button label="span 12" style="width: auto; background-color: #e5e9f2"></Button>
    </Col>
  </Row>

  <Row justify_items="center">
    <Col :span="4">
      <Button label="" style="width: auto; background-color: #d4dde6"></Button>
    </Col>
    <Col :span="4" style="width: auto">
      <Button label="" style="width: auto; background-color: #e5e9f2"></Button>
    </Col>
    <Col :span="4" style="width: auto">
      <Button label="" style="width: auto; background-color: #d4dde6"></Button>
    </Col>
  </Row>

  <Row>
    <Col :span="6">
      <Button label="span 6" style="width: auto; background-color: #d4dde6"></Button>
    </Col>
    <Col :span="6">
      <Button label="span 6" style="width: auto; background-color: #e5e9f2"></Button>
    </Col>
    <Col :span="6">
      <Button label="span 6" style="width: auto; background-color: #d4dde6"></Button>
    </Col>
    <Col :span="6">
      <Button label="span 6" style="width: auto; background-color: #e5e9f2"></Button>
    </Col>
  </Row>
</template>

<script setup>
import Col from "../../../src/ipywui/components/Col";
import Row from "../../../src/ipywui/components/Row";
import Button from "../../../src/ipywui/components/Button";
</script>