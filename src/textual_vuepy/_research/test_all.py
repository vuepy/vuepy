from vuepy import create_app, import_sfc

App = import_sfc("""
<template>
  <VBox>
    <Header />
    <VBox style="height: 1fr; overflow-y: scroll;">
      <Label label="--- Layouts ---" />
      <HBox style="height: 3; border: solid green;">
        <Label label="HBox Item 1" />
        <Label label="HBox Item 2" />
      </HBox>

# DataTable
<!--
      <DataTable :cols="['a', 'b', 'c']" 
                 :rows="[[1, 2, 3], [4, 5, 6], [7, 8, 9]]" />
-->

      <Label label="--- Inputs ---" />
      <Button label="Button" />
      <Checkbox label="Checkbox" />
      <Input placeholder="Input" />
      <MaskedInput template="99-99-9999" placeholder="MaskedInput (date)" />
      <Switch />
      <Select v-model='sel.value' :options="[('Option A', 'a'), ('Option B', 'b')]" />

# RadioSet
      <RadioSet>
        <RadioButton label="Radio 1" />
        <RadioButton label="Radio 2" />
      </RadioSet>

# OptionList
      <OptionList>
        <Option prompt="Option 1" />
        <Option prompt="Option 2" />
      </OptionList>
    
# SelectionList
      <SelectionList>
        <Selection prompt="Selection 1" value="1" />
        <Selection prompt="Selection 2" value="2" />
      </SelectionList>

      <Label label="--- Text & Display ---" />
      <Label label="Standard Label" />
      <Static>Static Widget Content</Static>
      <Digits value="1234.56" />
      <ProgressBar :total="100" />
      <Rule />
      <Sparkline :data="[1, 2, 4, 8, 16, 32]" />
      <Link text="Link (Google)" url="https://google.com" />
      
      <Label label="--- Text Editors / Viewers ---" />
      <TextArea />
      <Markdown markdown="# Markdown Heading\n* Italic\n* **Bold**" />
      <MarkdownViewer markdown="# Markdown Viewer\n## Subtitle\nText." />

# ListView
      <ListView>
        <ListItem><Label label="List Item 1" /></ListItem>
        <ListItem><Label label="List Item 2" /></ListItem>
      </ListView>

# Tree
      <Tree label="Tree Root">
        <Tree label="Node 1" />
        <Tree label="Node 2">
            <Tree label="Leaf" />
        </Tree>
      </Tree>
      <!-- DirectoryTree requires a valid path -->
      <DirectoryTree path="./" style="height: 10;" />
      
# Tabs
      <Tabs>
        <Tab label="Tab 1" id="tab1" />
        <Tab label="Tab 2" id="tab2" />
      </Tabs>

# TabbedContent
      <TabbedContent initial="pane2">
        <TabPane title="Pane1" id="pane1">
          <Label label="Content 1" />
        </TabPane>
        <TabPane title="Pane2" id="pane2">
          <Label label="Content 2" />
        </TabPane>
      </TabbedContent>
      
# Collapsible
      <Collapsible title="Collapsible">
        <Label label="Hidden Content" />
      </Collapsible>
 
 # ContentSwitcher
      <ContentSwitcher initial="c1">
        <Label id="c1" label="Content Switcher 1" />
        <Label id="c2" label="Content Switcher 2" />
      </ContentSwitcher>

# Log
      <Log />
# RichLog
      <RichLog />
      
      <Label label="--- Other ---" />
      <Placeholder />
      <Pretty :object="{'key': 'value', 'list': [1, 2, 3]}" />
      
      <!-- Panels (need context) -->
      <!-- <HelpPanel /> -->
      <!-- <KeyPanel /> -->
      
      <!-- Dialog (Hidden by default, open with ref/v-model) -->
      <Dialog>
        <Label label="I am a dialog" />
        <Button label="Close" />
      </Dialog>
      
      <LoadingIndicator />
      <!-- Welcome widget (usually full screen) -->
      <!-- <Welcome /> -->

    </VBox>
    <Footer />
  </VBox>
</template>
<script lang="py">
from vuepy import ref

sel = ref('b', debug_msg='sel')
</script>
<style>
/* CSS / TCSS styles */
</style>
""", raw_content=True)

app = create_app(App, backend='textual')
app.mount()

