<template>
  <Row>
    <Col :span="24">
      <Button label="span 24" style="width: auto; background-color: #9dacc1"></Button>
    </Col>
  </Row>

  <Row>
    <Col :span="12">
      <Button label="span 12" style="width: auto; background-color: #d4dde6"></Button>
    </Col>
    <Col :span="12">
      <Button label="span 12" style="width: auto; background-color: #e5e9f2"></Button>
    </Col>
  </Row>

  <Row>
    <Col :span="8">
      <Button label="span 8" style="width: auto; background-color: #d4dde6"></Button>
    </Col>
    <Col :span="8">
      <Button label="span 8" style="width: auto; background-color: #e5e9f2"></Button>
    </Col>
    <Col :span="8">
      <Button label="span 8" style="width: auto; background-color: #d4dde6"></Button>
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