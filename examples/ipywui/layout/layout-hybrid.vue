<template>
  <Row gutter="20px">
    <Col :span="16">
      <Button label="span 16" style="width: auto; background-color: #d4dde6"></Button>
    </Col>
    <Col :span="8">
      <Button label="span 8" style="width: auto; background-color: #e5e9f2"></Button>
    </Col>
  </Row>

  <Row gutter="20px">
    <Col :span="8">
      <Button label="span 8" style="width: auto; background-color: #d4dde6"></Button>
    </Col>
    <Col :span="8">
      <Button label="span 8" style="width: auto; background-color: #e5e9f2"></Button>
    </Col>
    <Col :span="4">
      <Button label="span 4" style="width: auto; background-color: #d4dde6"></Button>
    </Col>
    <Col :span="4">
      <Button label="span 4" style="width: auto; background-color: #e5e9f2"></Button>
    </Col>
  </Row>

  <Row gutter="20px">
    <Col :span="4">
      <Button label="span 4" style="width: auto; background-color: #d4dde6"></Button>
    </Col>
    <Col :span="16">
      <Button label="span 16" style="width: auto; background-color: #e5e9f2"></Button>
    </Col>
    <Col :span="4">
      <Button label="span 4" style="width: auto; background-color: #d4dde6"></Button>
    </Col>
  </Row>
</template>

<script setup>
import Col from "../../../src/ipywui/components/Col";
import Row from "../../../src/ipywui/components/Row";
import Button from "../../../src/ipywui/components/Button";
</script>