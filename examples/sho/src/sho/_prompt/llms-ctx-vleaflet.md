# vleaflet

vleaflet 是基于 Vue.py 和 ipyleaflet 开发的响应式地图组件库，在 Jupyter 中实现交互式地图。vleaflet 中的每个对象（包括地图、TileLayers、图层、控件等）都是响应式的：您可以从 Python 或浏览器动态更新属性。

## 安装

```sh
pip install 'vuepy-core[vleaflet]'
```

## 运行 

use 插件方式:

```python{2,7}
from vuepy import create_app, import_sfc
from vleaflet import leaflet

App= import_sfc('App.vue')  # 根据 App.vue 实际位置修改
app = create_app(App)
app.use(leaflet)
app.mount()
```

`%vuepy_run` 方式：

```python{2,4}
from vuepy.utils import magic
from vleaflet import leaflet

%vuepy_run app.vue --plugins leaflet
```

`%%vuepy_run` 方式：

```python{2,5}
from vuepy.utils import magic
from vleaflet import leaflet

# -- cell --
%%vuepy_run --plugins leaflet
<template>
  <vl-map :center="[53, 354]" />
</template>
```

# Map

## 基础用法

```vue
<template>
  <Slider v-model="zoom.value" description='zoom' :min=3 :max=13 />
  <p>zoom: {{ zoom.value }}, center: {{ center.value }}</p>

  <vl-map
    v-model:center="center.value"
    v-model:zoom="zoom.value"
    :zoom-control='False'
    :scroll-wheel-zoom='True'
    :keyboard="True"
    :basemap="basemaps.Esri.WorldTopoMap"
    style='width: 90%; height: 500px; border: 1px solid red;'
    ref=m
  >
    <template #controls>
      <vl-zoom-control position='topleft'/>
    </template>
    <template #layers>
        <vl-marker name='marker' :location='[53, 354]'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from ipyleaflet import basemaps, Marker
from vuepy import ref

m = ref(None)
zoom = ref(5)
center = ref((53, 354))

</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
|--------|------|------|--------|
| v-model:center | 地图中心点 | ^[Array]`[number, number]` | [0, 0] |
| v-model:zoom | 地图缩放级别 | ^[number] | 12 |
| max_zoom | 最大缩放级别 | ^[number] | null |
| min_zoom | 最小缩放级别 | ^[number] | null |
| zoom_snap | 缩放步长 | ^[number] | 1 |
| zoom_delta | 缩放增量 | ^[number] | 1 |
| crs | 坐标参考系统 | ^[enum]`'Earth'\|'EPSG3395'\|'EPSG3857'\|'EPSG4326'\|'Base'\|'Simple'` | 'EPSG3857' |
| dragging | 是否可拖动 | ^[boolean] | true |
| touch_zoom | 是否支持触摸缩放 | ^[boolean] | true |
| scroll_wheel_zoom | 是否支持滚轮缩放 | ^[boolean] | false |
| double_click_zoom | 是否支持双击缩放 | ^[boolean] | true |
| box_zoom | 是否支持框选缩放 | ^[boolean] | true |
| tap | 是否启用移动端点击支持 | ^[boolean] | true |
| tap_tolerance | 触摸容差 | ^[number] | 15 |
| world_copy_jump | 是否支持世界复制跳转 | ^[boolean] | false |
| close_popup_on_click | 点击地图时是否关闭弹窗 | ^[boolean] | true |
| bounce_at_zoom_limits | 是否在缩放限制时反弹 | ^[boolean] | true |
| keyboard | 是否支持键盘控制 | ^[boolean] | true |
| keyboard_pan_offset | 键盘平移偏移量 | ^[number] | 80 |
| keyboard_zoom_offset | 键盘缩放偏移量 | ^[number] | 1 |
| inertia | 是否启用惯性效果 | ^[boolean] | true |
| inertia_deceleration | 惯性减速率 | ^[number] | 3000 |
| inertia_max_speed | 最大惯性速度 | ^[number] | 1500 |
| zoom_control | 是否显示缩放控件 | ^[boolean] | true |
| attribution_control | 是否显示属性控件 | ^[boolean] | true |
| zoom_animation_threshold | 缩放动画阈值 | ^[number] | 4 |
| basemap | 底图样式 | ^[object] | {} |
| style | 自定义样式 | ^[string] | '' |

### 方法

| 方法名 | 说明 | 类型 |
|--------|------|------|
| add | 添加图层或控件 | `(item: any, index?: number) => void` |
| clear | 清除所有图层和控件 | `() => void` |
| fit_bounds | 设置地图视图以包含给定的地理边界 | `(bounds: any) => void` |
| remove | 移除图层或控件 | `(item: any) => void` |
| save | 将地图保存为HTML文件 | `(outfile: string, title: string) => void` |
| substitute | 替换地图上的图层或控件 | `(old: any, new_: any) => void` |

### Slots

| 插槽名 | 说明 |
|--------|------|
| layers | 地图图层插槽 |
| controls | 地图控件插槽 |

### Events

| 事件名 | 说明                  | 类型                                   |
| ---   | ---                  | ---                                    |



# Basemaps

在此页面中，您可以查看 ipyleaflet 提供的默认底图选项。当然，您也可以通过创建自定义的 `TileLayer` 来使用其他地图服务提供商。
这些底图均源自 [xyzservices](https://xyzservices.readthedocs.io/) 这个 Python 包。
## 基础用法
```vue
<template>
  <vl-map
    :center="(38.128, 2.588)"
    :zoom="5"
    :basemap="basemap"
  >
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from ipyleaflet import basemaps

# basemap = basemaps.OpenStreetMap.France
# basemap = basemaps.OpenStreetMap.HOT
# basemap = basemaps.Gaode.Normal
# basemap = basemaps.OpenTopoMap
# basemap = basemaps.Gaode.Satellite
# basemap = basemaps.Esri.WorldStreetMap
# basemap = basemaps.Esri.DeLorme
# basemap = basemaps.Esri.WorldTopoMap
# basemap = basemaps.Esri.WorldImagery
# basemap = basemaps.Esri.NatGeoWorldMap
# basemap = basemaps.CartoDB.DarkMatter
# basemap = basemaps.CartoDB.Positron
# basemap = basemaps.NASAGIBS.ModisTerraTrueColorCR
# basemap = basemaps.NASAGIBS.ModisTerraBands367CR
# basemap = basemaps.NASAGIBS.ModisTerraBands721CR
# more https://ipyleaflet.readthedocs.io/en/latest/map_and_basemaps/basemaps.html
basemap = basemaps.OpenStreetMap.Mapnik
</script>

```



# Local Tile Layer

## 基础用法

```vue
<template>
  <vl-map :center="[0, 0]" :zoom='1'>
    <template #layers>
      <vl-local-tile-layer :path="path" name='local'/>
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy.utils import magic

# for jupyterlab
# path = "../tiles/{z}-{x}-{y}.jpg"
path = "/files/nb_llm/pyvue/examples/vleaflet/layers/tiles/{z}-{x}-{y}.jpg"
</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 验证规则 |
|--------|------|------|--------|------|----------|
| path | 本地 tile 路径模板 | string | - | 是 | 需包含{z}/{x}/{y}占位符 |
| name | 图层名称 | string | '' | 否 | - |
| min_zoom | 最小显示缩放级别 | number | 0 | 否 | - |
| max_zoom | 最大显示缩放级别 | number | 18 | 否 | - |
| max_native_zoom | tile 源最大原生缩放级别 | number | null | 否 | - |
| min_native_zoom | tile 源最小原生缩放级别 | number | null | 否 | - |
| bounds | 显示范围边界<br>[西南角, 东北角] | [[number,number],[number,number]] | null | 否 | 经纬度坐标 |
| tile_size | tile 尺寸(像素) | number | 256 | 否 | - |
| attribution | 数据源属性说明 | string | '' | 否 | - |
| no_wrap | 是否禁止跨180度经线 | boolean | false | 否 | - |
| tms | 是否使用TMS tile坐标系 | boolean | false | 否 | 反转Y轴编号 |
| zoom_offset | tile URL缩放级别偏移量 | number | 0 | 否 | - |
| show_loading | 是否显示加载指示器 | boolean | false | 否 | - |
| loading | tile 是否正在加载 | boolean | false | 否 | - |
| detect_retina | 是否检测Retina屏幕 | boolean | false | 否 | - |
| opacity | 图层透明度 | number | 1.0 | 否 | 0-1之间 |
| visible | 是否可见 | boolean | true | 否 | - |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| - | - | - |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| - | - |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | - | - | - |


# Polygon

## 基础用法

```vue
<template>
  <vl-map :center="[37, -109]" :zoom=5>
    <template #layers>
      <vl-polygon
        :locations="[(37, -100), (43, -100), (43, -90)]"
        :color='color.value',
        :fill='True'
        name='polygon'/>
      <vl-polygon
        :locations="[(30, -110), (35, -110), (35, -122)]"
        :color='color.value',
        :fill='True'
        :transform="True"
        name='editable polygon'/>
      <vl-polygon
        :locations="paths"
        color='red',
        :fill='False'
        name='polygon with holes'/>
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref

color = ref('green')
paths = [
    [(37, -109.05), (41, -109.03), (41, -102.05), (37, -102.04)],
    [(37.29, -108.58), (40.71, -108.58), (40.71, -102.50), (37.29, -102.50)],
]

def on_click():
    color.value = 'red'
</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 验证规则 |
|--------|------|------|--------|------|----------|
| locations | 多边形顶点坐标数组 | Array<[number, number]> | - | 是 | 每个元素必须是[经度,纬度] |
| name | 图层名称 | string | '' | 否 | - |
| color | 边框颜色 | string | '#0000ff' | 否 | CSS颜色值 |
| scaling | 是否可缩放 | boolean | true | 否 | - |
| rotation | 是否可旋转 | boolean | true | 否 | - |
| uniform_scaling | 是否等比例缩放 | boolean | true | 否 | - |
| fill | 是否填充 | boolean | false | 否 | - |
| fill_color | 填充颜色 | string | null | 否 | CSS颜色值 |
| fill_opacity | 填充不透明度 | number | 0.2 | 否 | 0-1之间 |
| fill_rule | 填充规则 | string | 'evenodd' | 否 | 'evenodd'或'nonzero' |
| transform | 是否可变形 | boolean | false | 否 | 修正原文档False为false |
| smooth_factor | 平滑强度 | number | 1.0 | 否 | - |
| draggable | 是否可拖动 | boolean | false | 否 | - |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| - | - | - |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| - | - |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | - | - | - |


# Polyline

## 基础用法

```vue
<template>
  <Button @click='on_click()'>Switch color</Button>
  <vl-map :center="[42.5, -41]" :zoom=2>
    <template #layers>
      <vl-polyline
        :locations="path"
        :color='color.value',
        :fill='False'
        name='polyline' />
      <vl-polyline
        :locations="paths"
        color='red',
        :fill='False'
        name='multi polyline'/>
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref

path = [
   [43.51, -112.68],
   [33.77, -112.43],
   [34.04, -108.22],
]
paths = [
   [[45.51, -122.68],
    [37.77, -122.43],
    [34.04, -118.2]],
   [[40.78, -73.91],
    [41.83, -87.62],
    [32.76, -96.72]]
]
color = ref('green')

def on_click():
    color.value = 'red'
</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 验证规则 |
|--------|------|------|--------|------|----------|
| locations | 折线顶点坐标数组 | Array<[number, number]> | - | 是 | 每个元素必须是[经度,纬度] |
| name | 图层名称 | string | '' | 否 | - |
| color | 线条颜色 | string | '#0000ff' | 否 | CSS颜色值 |
| scaling | 是否可缩放 | boolean | true | 否 | - |
| rotation | 是否可旋转 | boolean | true | 否 | - |
| uniform_scaling | 是否等比例缩放 | boolean | true | 否 | - |
| fill | 是否填充(对折线无效) | boolean | false | 否 | 保留属性但实际无效 |
| fill_color | 填充颜色(对折线无效) | string | null | 否 | 保留属性但实际无效 |
| fill_opacity | 填充不透明度(对折线无效) | number | 0.2 | 否 | 保留属性但实际无效 |
| fill_rule | 填充规则(对折线无效) | string | 'evenodd' | 否 | 保留属性但实际无效 |
| transform | 是否可变形 | boolean | false | 否 | - |
| smooth_factor | 平滑强度 | number | 1.0 | 否 | 值越大越平滑 |
| draggable | 是否可拖动 | boolean | false | 否 | - |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| - | - | - |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| - | - |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | - | - | - |


# Circle

## 基础用法

```vue
<template>
  <Button @click='on_click()'>Switch color</Button>
  <vl-map :center="[53, 354]" :zoom=5>
    <template #layers>
      <vl-circle
        :location="(50, 354)"
        :radius="200000"
        :color='color.value',
        :fill='False'
        name='circle'
      />
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref

color = ref('green')

def on_click():
    color.value = 'red'
</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 验证规则/备注 |
|--------|------|------|--------|------|--------------|
| location | 圆心坐标[纬度,经度] | [float, float] | [0,0] | 是 | 必须包含2个数字元素 |
| radius | 圆半径(单位：米) | Number | - | 是 | 必须为二维坐标数组 |
| name | 图层名称 | string | '' | 否 | - |
| color | 边框颜色 | string | '#0000ff' | 否 | CSS颜色值 |
| scaling | 是否可缩放 | boolean | true | 否 | - |
| rotation | 是否可旋转 | boolean | true | 否 | - |
| uniform_scaling | 是否保持比例缩放 | boolean | true | 否 | - |
| fill | 是否填充 | boolean | false | 否 | - |
| fill_color | 填充颜色 | string | null | 否 | CSS颜色值 |
| fill_opacity | 填充不透明度 | number | 0.2 | 否 | 0-1之间的值 |
| fill_rule | 填充规则 | string | 'evenodd' | 否 | 'evenodd'或'nonzero' |
| transform | 是否可变形 | boolean | false | 否 | 原文档为False(应小写) |
| smooth_factor | 平滑强度 | number | 1.0 | 否 | - |
| draggable | 是否可拖动 | boolean | false | 否 | - |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|

### 插槽

| 插槽名 | 说明 |
|--------|------|

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|


# Tile Layer

## 基础用法

```vue
<template>
  <vl-map :center="[52.204793, 360.121558]">
    <template #layers>
      <vl-tile-layer :url="url1" name='World Street' @load='on_load'/>
      <vl-tile-layer :url="url2" name='World Topo' :base="True"/>
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from ipyleaflet import basemaps

# from xyzservices.lib.TileProvider
st_map1 = basemaps.Esri.WorldStreetMap
url1 = st_map1.build_url(time='2025-04-01')

url2 = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}'

def on_load(**kwargs):
    print(kwargs) #  {'event': 'load'}
</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 备注 |
|--------|------|------|--------|------|------|
| url | tile 服务URL模板 | string | "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" | 是 | 需包含{z}/{x}/{y}占位符 |
| base | 是否作为底图 | boolean | false | 否 | - |
| name | 图层名称 | string | '' | 否 | - |
| min_zoom | 最小显示级别 | number | 0 | 否 | - |
| max_zoom | 最大显示级别 | number | 18 | 否 | - |
| max_native_zoom | tile 源最大原生级别 | number | null | 否 | - |
| min_native_zoom | tile 源最小原生级别 | number | null | 否 | - |
| bounds | 显示范围边界<br>[西南角,东北角] | [[number,number],[number,number]] | null | 否 | 经纬度坐标 |
| tile_size | tile 尺寸(像素) | number | 256 | 否 | - |
| attribution | 数据源属性说明 | string | '' | 否 | - |
| no_wrap | 是否禁止跨180度经线 | boolean | false | 否 | - |
| tms | 是否使用TMS tile坐标系 | boolean | false | 否 | 反转Y轴编号 |
| zoom_offset | tile URL缩放级别偏移 | number | 0 | 否 | - |
| show_loading | 是否显示加载指示器 | boolean | false | 否 | - |
| loading | tile 是否正在加载 | boolean | false | 否 | - |
| detect_retina | 是否检测Retina屏幕 | boolean | false | 否 | - |
| opacity | 图层透明度 | number | 1.0 | 否 | 0-1之间 |
| visible | 是否可见 | boolean | true | 否 | - |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| load | tile加载完成时触发 | - |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| - | - |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| redraw | 强制重绘 | - | void |


# Velocity

To visualize the direction and intensity of arbitrary velocities
## 基础用法

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 备注 |
|--------|------|------|--------|------|------|
| data | 速度场数据源 | Object | - | 是 | 必须包含速度场数据 |
| name | 图层名称 | string | '' | 否 | - |
| zonal_speed | 纬向速度变量名 | string | '' | 否 | 数据源中的字段名 |
| meridional_speed | 经向速度变量名 | string | '' | 否 | 数据源中的字段名 |
| latitude_dimension | 纬度维度名 | string | '' | 否 | 数据源中的纬度字段 |
| longitude_dimension | 经度维度名 | string | '' | 否 | 数据源中的经度字段 |
| display_values | 是否显示悬停数值 | boolean | true | 否 | - |
| display_options | 显示配置选项 | Object | `{velocity_type: 'Global Wind',display_position: 'bottomleft',display_empty_string: 'No wind data',angle_convention: 'bearingCW',speed_unit: 'kts'}` | 否 | 支持多种显示配置 |
| min_velocity | 最小速度值 | number | 0 | 否 | 用于颜色标尺 |
| max_velocity | 最大速度值 | number | 10 | 否 | 用于颜色标尺 |
| velocity_scale | 速度缩放系数 | number | 0.005 | 否 | 控制粒子动画 |
| color_scale | 自定义颜色标尺 | Array\<string\> | [] | 否 | 十六进制/RGB颜色数组 |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| - | - | - |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| - | - |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | - | - | - |

ref: https://ipyleaflet.readthedocs.io/en/latest/layers/velocity.html


# GeoData

Layer created from a GeoPandas dataframe.
## 基础用法

```vue
<template>
  <vl-map :center="[46.91, 7.43]" :zoom=15 >
    <template #layers>
      <vl-geo-data name='geo data' @click=on_click
                   :geo_dataframe="gdf" :style='style' 
                   :hover_style='hover_style'
                   :point_style='point_style' />
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
import geopandas, pandas as pd, numpy as np

numpoints = 10
center = (7.43, 46.91)

df = pd.DataFrame(
    {'Conc': 1 * np.random.randn(numpoints) + 17,
     'Longitude': 0.0004 * np.random.randn(numpoints) + center[0],
     'Latitude': 0.0004 * np.random.randn(numpoints) + center[1]})

gdf = geopandas.GeoDataFrame(
    df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))

style ={
    'color': 'black',
    'radius':8,
    'fillColor': '#3366cc',
    'opacity':0.5,
    'weight':1.9,
    'dashArray':'2',
    'fillOpacity':0.6
}
point_style = {
    'radius': 5,
    'color': 'red',
    'fillOpacity': 0.8,
    'fillColor': 'blue',
    'weight': 3
}
hover_style = {'fillColor': 'red' , 'fillOpacity': 0.2}

def on_click(**kwargs):
    print(kwargs)

</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 备注 |
|--------|------|------|--------|------|------|
| geo_dataframe | 使用的GeoPandas数据框 | Object | - | 是 | 必须包含有效的GeoDataFrame数据 |
| name | 图层名称 | string | '' | 否 | - |
| style | 应用到要素的额外样式 | Object | `{}` | 否 | 支持Leaflet样式对象 |
| hover_style | 鼠标悬停时的要素样式 | Object | `{}` | 否 | 支持Leaflet样式对象 |
| point_style | 应用到点要素的额外样式 | Object | `{}` | 否 | 支持Leaflet样式对象 |
| style_callback | 要素样式回调函数 | Function | null | 否 | 接收feature参数，返回样式对象 |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| click | 点击要素时触发 | feature: 被点击的要素数据 |
| hover | 鼠标悬停要素时触发 | feature: 被悬停的要素数据 |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| - | - |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | - | - | - |


# Marker Cluster

## 基础用法

```vue
<template>
  <vl-map :center="[50, 0]" :zoom=5>
    <template #layers>
      <vl-marker-cluster name='marker cluster'>
        <vl-marker :location="(48, -2)"/>
        <vl-marker :location="(50, 0)"/>
        <vl-marker :location="(52, 2)"/>
      </vl-marker-cluster>
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 备注 |
|--------|------|------|--------|------|------|
| name | 图层名称 | string | '' | 否 | - |
| max_cluster_radius | 聚类最大半径(像素) | number | 80 | 否 | 值越小聚类越多 |
| spiderfy_on_max_zoom | 最大缩放级别时展开聚类 | boolean | true | 否 | 显示所有标记 |
| show_coverage_on_hover | 悬停时显示覆盖范围 | boolean | true | 否 | - |
| zoom_to_bounds_on_click | 点击时缩放到聚类范围 | boolean | true | 否 | - |
| disable_clustering_at_zoom | 禁用聚类的缩放级别 | number | 18 | 否 | 该级别以下不聚类 |
| remove_outside_visible_bounds | 移出视口的标记 | boolean | true | 否 | 提升性能 |
| animate | 启用动画效果 | boolean | true | 否 | 需浏览器支持 |
| animate_adding_markers | 添加标记时动画 | boolean | false | 否 | 影响批量添加性能 |
| spider_leg_polyline_options | 样式配置 | dict | ^[dict]`{weight:1.5,color: #222,opacity:0.5}` | 否 | 折线样式 |
| spiderfy_distance_multiplier | 距离系数 | number | 1 | 否 | 大图标需调整 |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|

### 插槽

| 插槽名 | 说明 |
|--------|------|
| default | 包含要聚类的标记 |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|


# Layer-Like Objects

The ipyleaflet.Map.add() method supports “layer-like” objects; meaning any object with an as_leaflet_layer method. This interface can be especially useful for downstream developers who want their users to more easily be able to add their objects to an ipyleaflet.Map.

Downstream objects should implement an `as_leaflet_layer` method that returns an `ipyleaflet` type capable of being added to the Map.
## 基础用法

```vue
<template>
  <vl-map :center="center" :zoom=2 ref='m'>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
import numpy as np
from vuepy import ref, onMounted


class MyHeatMap:
    def __init__(self, name, points, values, radius=20):
        self.name = name
        self.points = points
        self.values = values
        self.radius = radius

    @property
    def data(self):
        return np.column_stack((self.points, self.values))

    def as_leaflet_layer(self):
        from ipyleaflet import Heatmap
        return Heatmap(
            name=self.name,
            locations=self.data.tolist(),
            radius=self.radius,
        )

m = ref(None)
center = [0, 0]

n = 1000
data = MyHeatMap(
    'layer-like',
    np.random.uniform(-80, 80, (n, 2)),
    np.random.uniform(0, 1000, n),
)

@onMounted
def add_layer():
    m.value.add(data)
    
</script>

```



# Marker 

## 基础用法

```vue
<template>
  <vl-map :center="[50, 0]" :zoom=5>
    <template #layers>
      <vl-marker v-model="loc.value" name='mark1' @move="on_move" title='move'/>
      <vl-marker :location="(50, 0)" name='with popup' @click='on_click'>
          <template #popup>
            <p>mark1 loc {{ loc.value }}</p>
            <Button>ok</Button>
          </template>
      </vl-marker>
      <vl-marker :location='(52, 2)' name='with icon'>
        <template #icon>
         <vl-awesome-icon name='bus'/>
        </template>
      </vl-marker>
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref

loc = ref((48, -2))

def on_move(**kwargs):
    print(kwargs) # {'event': 'move', 'location': [49, -5]}

def on_click(**kwargs):
    print(kwargs)
</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 验证规则/备注 |
|--------|------|------|--------|------|--------------|
| location | 标记位置[纬度,经度] | [number, number] | [0,0] | 是 | 支持v-model绑定 |
| name | 图层名称 | string | '' | 否 | - |
| opacity | 标记透明度 | number | 1.0 | 否 | 0-1之间 |
| visible | 是否可见 | boolean | true | 否 | - |
| icon | 图标配置 | Object | null | 否 | 支持自定义图标 |
| draggable | 是否可拖动 | boolean | true | 否 | - |
| keyboard | 是否支持键盘操作 | boolean | true | 否 | - |
| title | 悬停提示文本 | string | '' | 否 | - |
| alt | 无障碍文本 | string | '' | 否 | - |
| rotation_angle | 旋转角度 | number | 0 | 否 | 角度值 |
| rotation_origin | 旋转原点 | string | '' | 否 | CSS格式 |
| z_index_offset | z-index偏移量 | number | 0 | 否 | - |
| rise_offset | 悬停时上升偏移量 | number | 250 | 否 | 像素单位 |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| click | 鼠标点击时触发 | event, type, coordinates |
| move | 标记移动时触发 | newLocation: 新位置[lat,lng] |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| icon | 自定义标记图标 |
| popup | 自定义弹出内容 |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | - | - | - |

ref: https://ipyleaflet.readthedocs.io/en/latest/layers/marker.html


# Rectangle

## 基础用法

```vue
<template>
  <Button @click='on_click()'>Switch color</Button>
  <vl-map :center="[53, 354]" :zoom=5>
    <template #layers>
      <vl-rectangle
        :bounds="[(52, 354), (53, 360)]"
        :color='color.value',
        :fill='False'
        name='rectangle'/>
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref

color = ref('green')

def on_click():
    color.value = 'red'
</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 验证规则 |
|--------|------|------|--------|------|----------|
| bounds | 矩形范围边界<br>[西南角, 东北角] | [[number,number], [number,number]] | - | 是 | 必须包含2个经纬度坐标 |
| name | 图层名称 | string | '' | 否 | - |
| color | 边框颜色 | string | '#0000ff' | 否 | CSS颜色值 |
| scaling | 是否可缩放 | boolean | true | 否 | - |
| rotation | 是否可旋转 | boolean | true | 否 | - |
| uniform_scaling | 是否等比例缩放 | boolean | true | 否 | - |
| fill | 是否填充 | boolean | false | 否 | - |
| fill_color | 填充颜色 | string | null | 否 | CSS颜色值 |
| fill_opacity | 填充不透明度 | number | 0.2 | 否 | 0-1之间 |
| fill_rule | 填充规则 | string | 'evenodd' | 否 | 'evenodd'或'nonzero' |
| transform | 是否可变形 | boolean | false | 否 | 修正原文档False为false |
| smooth_factor | 平滑强度 | number | 1.0 | 否 | - |
| draggable | 是否可拖动 | boolean | false | 否 | - |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| - | - | - |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| - | - |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | - | - | - |


# Popup

## 基础用法

```vue
<template>
  <Button @click='open_or_close()'>popup: open or close</Button>
  <vl-map :center="p" :zoom=9>
    <template #layers>
      <vl-popup name='popup' :location='[52.204793, 360.121558]' ref='popup'>
        <p>popup: {{ loc.value }}</p>
      </vl-popup>
      <vl-marker :location='p' name='marker1' @move='on_move'/>
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref

p = [52.1, 359.9]

loc = ref(str(p))
popup = ref(None)
is_open = True

def open_or_close():
    nonlocal is_open
    if is_open:
        popup.value.close_popup()
    else:
        popup.value.open_popup()
    is_open = not is_open
        

def on_move(**kwargs):
    print(kwargs) # {'event': 'move', 'location': [52, 360]}
    loc.value = str(kwargs)

</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 验证规则 |
|--------|------|------|--------|------|----------|
| location | 弹出框位置[纬度,经度] | [number, number] | [0,0] | 是 | 必须包含2个数字 |
| max_width | 最大宽度(像素) | number | 300 | 否 | - |
| min_width | 最小宽度(像素) | number | 50 | 否 | - |
| max_height | 最大高度(像素) | number | null | 否 | - |
| auto_pan | 是否自动平移地图 | boolean | true | 否 | - |
| auto_pan_padding | 自动平移边距[水平,垂直] | [number, number] | [5,5] | 否 | 像素单位 |
| keep_in_view | 是否保持在视图中 | boolean | false | 否 | - |
| close_button | 是否显示关闭按钮 | boolean | true | 否 | - |
| auto_close | 是否自动关闭 | boolean | true | 否 | 交互时自动关闭 |
| close_on_escape_key | 按ESC键关闭 | boolean | true | 否 | - |
| close_on_click | 点击外部关闭 | boolean | null | 否 | null时自动判断 |
| className | 自定义CSS类名 | string | '' | 否 | - |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| - | - | - |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| default | 弹出框内容 |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| close_popup | 关闭弹出框 | - | void |
| open_popup | 打开弹出框 | location: 可选新位置 | void |


# Layer Group

## 基础用法

```vue
<template>
  <vl-map :center="[53, 354]" :zoom=5>
    <template #layers>
      <vl-layer-group name='layer group'>
        <vl-rectangle :bounds="[(52, 354), (53, 360)]"/>
        <vl-circle :location="(50, 370)" :radius="50000"/>
        <vl-marker :location="(50, 354)"/>
      </vl-layer-group>
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 |
|--------|------|------|--------|------|
| name | 图层组名称 | string | '' | 否 |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| - | - | - |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| default | 自定义图层内容 |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| add | 添加图层到组 | layer: 图层对象 | void |
| clear | 清空所有图层 | - | void |
| remove | 移除指定图层 | rm_layer: 要移除的图层 | void |
| substitute | 替换图层 | old: 旧图层<br>new_: 新图层 | void |


# Circle Marker

## 基础用法

```vue
<template>
  <Button @click='on_click()'>Switch color</Button>
  <vl-map :center="[53, 354]" :zoom=5>
    <template #layers>
      <vl-circle-marker
        :location="(50, 360)"
        :radius="50"
        :color='color.value',
        :fill='False'
        name='circle marker'/>
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref

color = ref('green')

def on_click():
    color.value = 'red'
</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 验证规则 |
|--------|------|------|--------|------|----------|
| location | 标记位置[纬度,经度] | [float, float] | [0,0] | 是 | 必须为包含2个数字的数组 |
| radius | 圆半径(像素) | number | - | 是 | 必须为数字 |
| name | 图层名称 | string | '' | 否 | - |
| color | 边框颜色 | string | '#0000ff' | 否 | CSS颜色值 |
| scaling | 是否可缩放 | boolean | true | 否 | - |
| rotation | 是否可旋转 | boolean | true | 否 | - |
| uniform_scaling | 是否保持比例缩放 | boolean | true | 否 | - |
| fill | 是否填充 | boolean | false | 否 | - |
| fill_color | 填充颜色 | string | null | 否 | CSS颜色值 |
| fill_opacity | 填充不透明度 | number | 0.2 | 否 | 0-1之间的值 |
| fill_rule | 填充规则 | string | 'evenodd' | 否 | 'evenodd'或'nonzero' |
| transform | 是否可变形 | boolean | false | 否 | - |
| smooth_factor | 平滑强度 | number | 1.0 | 否 | - |
| draggable | 是否可拖动 | boolean | false | 否 | - |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|

### 插槽

| 插槽名 | 说明 |
|--------|------|

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|



# GeoJson 

Layer created from a GeoJSON data structure.

## 基础用法

```vue
<template>
  <vl-map :center="[50.6252978589571, 0.34580993652344]" :zoom=3>
    <template #layers>
      <vl-geo-json name='geo json' @click=onclick
                   :data="data" :style='style' :hover_style='hover_style'
                   :style_callback='random_color'/>
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
import os
import json
import random
import requests

if not os.path.exists('europe_110.geo.json'):
    url = 'https://github.com/jupyter-widgets/ipyleaflet/raw/master/examples/europe_110.geo.json'
    r = requests.get(url)
    with open('europe_110.geo.json', 'w') as f:
        f.write(r.content.decode("utf-8"))

with open('europe_110.geo.json', 'r') as f:
    data = json.load(f)

def random_color(feature):
    return {
        'color': 'black',
        'fillColor': random.choice(['red', 'yellow', 'green', 'orange']),
    }

style = {
    'opacity': 1, 
    'dashArray': '9',
    'fillOpacity': 0.1,
    'weight': 1,
}
hover_style={
    'color': 'white', 
    'dashArray': '0',
    'fillOpacity': 0.5,
}

def onclick(**kwargs):
    print(kwargs)

</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 备注 |
|--------|------|------|--------|------|------|
| data | GeoJSON数据结构 | Object | - | 是 | 必须包含有效的GeoJSON数据 |
| name | 图层名称 | string | '' | 否 | - |
| style | 应用到要素的基础样式 | Object | `{}` | 否 | 支持Leaflet Path样式选项 |
| hover_style | 鼠标悬停时的要素样式 | Object | `{}` | 否 | 支持Leaflet Path样式选项 |
| point_style | 点要素的特殊样式 | Object | `{}` | 否 | 支持Leaflet Path样式选项 |
| style_callback | 动态样式回调函数 | Function | null | 否 | `(feature) => styleObject` |

### 事件

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| click | 要素点击事件 | `{ feature: GeoJSONFeature, layer: L.Layer }` |
| hover | 要素悬停事件 | `{ feature: GeoJSONFeature, layer: L.Layer }` |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| - | - |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | - | - | - |


# Icon Glass

## 基础用法

```vue
<template>
  <Slider v-model=radius.value description='radius' :min=50 :max=100 />
  <Slider v-model=zoom.value description='zoom' :min=1 :max=5 />
  <vl-map :center="[52.204793, 360.121558]">
    <template #layers>
      <vl-magnifying-glass name='glass' :radius="radius.value" :zoom_offset="zoom.value">
        <vl-tile-layer :url="url2" name='World Topo'/>
      </vl-magnifying-glass>
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref

radius = ref(60)
zoom = ref(1)

url2 = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}'

</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 验证规则/备注 |
|--------|------|------|--------|------|--------------|
| radius | 放大镜半径(像素) | number | 100 | 否 | - |
| zoom_offset | 主地图与放大镜的缩放级别差 | number | 3 | 否 | 正值表示放大 |
| fixed_position | 是否固定位置 | boolean | false | 否 | true时不跟随鼠标 |
| lat_lng | 初始位置[纬度,经度] | [number,number] \| null | [0,0] | 否 | 固定位置时使用 |
| fixed_zoom | 固定缩放级别 | number \| null | null | 否 | -1表示禁用 |
| layers | 放大镜显示的图层数组 | Array\<Object\> | [] | 否 | 不应已添加到地图 |
| name | 图层名称 | string | '' | 否 | - |
| visible | 是否可见 | boolean | true | 否 | - |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| - | - | - |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| default | 自定义放大镜内容图层 |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | - | - | - |


# Image overlay and Video overlay

## 基础用法

```vue
<template>
  <vl-map :center="[25, -115]" :zoom=4>
    <template #layers>
      <vl-image-overlay url="https://www.vuepy.org/images/vuepy-logo.svg" 
                        name='image'
                        :bounds="((13, -130), (32, -100))"/>
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
</script>

```

```vue
<template>
  <vl-map :center="[25, -115]" :zoom=4>
    <template #layers>
      <vl-video-overlay url="https://www.mapbox.com/bites/00188/patricia_nasa.webm" 
                        name='video'
                        :bounds="((13, -130), (32, -100))" />
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
</script>

```

## ImageOverlay

### API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 验证规则 |
|--------|------|------|--------|------|----------|
| url | 图片资源URL(本地或远程) | string | '' | 是 | 必须为有效URL |
| bounds | 图片覆盖范围边界<br>[西南角,东北角] | [[number,number], [number,number]] | [[0,0],[0,0]] | 是 | 必须为2个经纬度坐标点 |
| name | 图层名称 | string | '' | 否 | - |
| attribution | 图片属性说明 | string | '' | 否 | - |
| alt | 图片替代文本 | string | '' | 否 | - |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| - | - | - |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| - | - |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | - | - | - |

## VideoOverlay API

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 验证规则 |
|--------|------|------|--------|------|----------|
| url | 视频资源URL(本地或远程) | string \| Array\<string\> | '' | 是 | 单个URL或多个视频URL数组 |
| bounds | 视频覆盖范围边界<br>[西南角, 东北角] | [[number,number], [number,number]] | [[0,0],[0,0]] | 是 | 必须为2个经纬度坐标点 |
| name | 图层名称 | string | '' | 否 | - |
| attribution | 视频属性说明 | string | '' | 否 | - |
| alt | 视频替代文本 | string | '' | 否 | 视频无法显示时展示 |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|

### 插槽

| 插槽名 | 说明 |
|--------|------|
| - | - |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|


# Vector Tile Layer

## 基础用法

```vue
<template>
  <vl-map :center="center" :zoom=9 ref='m'>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from ipyleaflet import VectorTileLayer
from traitlets import Unicode
from vuepy import ref, onMounted

m = ref(None)
center = [52.204793, 360.121558]

# This is a custom VectorTileLayer subclass, allowing to pass our api key to the url
class CustomVectorTileLayer(VectorTileLayer):
    api_key = Unicode('gCZXZglvRQa6sB2z7JzL1w').tag(sync=True, o=True)

water_style = dict(
fill="true",
weight=1,
fillColor="#06cccc",
color="#06cccc",
fillOpacity=0.2,
opacity=0.4,
)

waterway_style = dict(
    weight=1, fillColor="#2375e0", color="#2375e0", fillOpacity=0.2, opacity=0.4
)

admin_style = dict(
    weight=1, fillColor="pink", color="pink", fillOpacity=0.2, opacity=0.4
)

landcover_style = dict(
    fill="true",
    weight=1,
    fillColor="#53e033",
    color="#53e033",
    fillOpacity=0.2,
    opacity=0.4,
)

landuse_style = dict(
    fill="true",
    weight=1,
    fillColor="#e5b404",
    color="#e5b404",
    fillOpacity=0.2,
    opacity=0.4,
)

park_style = dict(
    fill="true",
    weight=1,
    fillColor="#84ea5b",
    color="#84ea5b",
    fillOpacity=0.2,
    opacity=0.4,
)

boundary_style = dict(
    weight=1, fillColor="#c545d3", color="#c545d3", fillOpacity=0.2, opacity=0.4
)

aeroway = dict(
    weight=1, fillColor="#51aeb5", color="#51aeb5", fillOpacity=0.2, opacity=0.4
)

road = dict(
    weight=1, fillColor="#f2b648", color="#f2b648", fillOpacity=0.2, opacity=0.4
)

transit = dict(
    weight=0.5, fillColor="#f2b648", color="#f2b648", fillOpacity=0.2, opacity=0.4
)

buildings = dict(
    fill="true",
    weight=1,
    fillColor="#2b2b2b",
    color="#2b2b2b",
    fillOpacity=0.2,
    opacity=0.4,
)

water_name = dict(
    weight=1, fillColor="#022c5b", color="#022c5b", fillOpacity=0.2, opacity=0.4
)

transportation_name = dict(
    weight=1, fillColor="#bc6b38", color="#bc6b38", fillOpacity=0.2, opacity=0.4
)

place = dict(
    weight=1, fillColor="#f20e93", color="#f20e93", fillOpacity=0.2, opacity=0.4
)

housenumber = dict(
    weight=1, fillColor="#ef4c8b", color="#ef4c8b", fillOpacity=0.2, opacity=0.4
)

poi = dict(weight=1, fillColor="#3bb50a", color="#3bb50a", fillOpacity=0.2, opacity=0.4)

earth = dict(
    fill="true",
    weight=1,
    fillColor="#c0c0c0",
    color="#c0c0c0",
    fillOpacity=0.2,
    opacity=0.4,
)

url = 'https://tile.nextzen.org/tilezen/vector/v1/512/all/{z}/{x}/{y}.mvt?api_key={apiKey}'
vector_tile_layer_styles = dict(
    water=water_style,
    waterway=waterway_style,
    admin=admin_style,
    andcover=landcover_style,
    landuse=landuse_style,
    park=park_style,
    boundaries=boundary_style,
    aeroway=aeroway,
    roads=road,
    transit=transit,
    buildings=buildings,
    water_name=water_name,
    transportation_name=transportation_name,
    places=place,
    housenumber=housenumber,
    pois=poi,
    earth=earth
)

vl = CustomVectorTileLayer(
    name='custom', url=url, vector_tile_layer_styles=vector_tile_layer_styles)

@onMounted
def add_layer():
    m.value.add(vl)
    
</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 备注 |
|--------|------|------|--------|------|------|
| url | 矢量tile服务URL | string | - | 是 | 必须为有效矢量瓦片服务地址 |
| name | 图层名称 | string | '' | 否 | - |
| attribution | 数据源属性说明 | string | '' | 否 | - |
| vector_tile_layer_styles | 矢量数据样式配置 | Object | `{}` | 否 | 支持Mapbox GL样式规范 |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| - | - | - |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| default | 自定义图层内容 |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| redraw | 强制重绘矢量tile | - | void |

ref: // https://ipyleaflet.readthedocs.io/en/latest/layers/vector_tile.html



# DivIcon

## 基础用法

```vue
<template>
  <vl-map :center="p">
    <template #layers>
      <vl-marker :location='p' name='div icon' @move='on_move'>
        <template #icon>
          <vl-div-icon :icon_size='[100, 100]' :icon_anchor='[22,94]'>
            <p>hello</p>
          </vl-div-icon>
        </template>
      </vl-marker>
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref

p = [52.204793, 360.121558]

loc = ref('')

def on_move(**kwargs):
    print(kwargs)
    loc.value = str(kwargs)

</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 验证规则 |
|--------|------|------|--------|------|----------|
| html | 自定义HTML内容 | string | '' | 否 | - |
| icon_size | 图标大小[宽,高](像素) | [number, number] | null | 否 | 必须为包含2个数字的数组 |
| icon_anchor | 图标锚点坐标[x,y] | [number, number] | null | 否 | 必须为包含2个数字的数组 |
| popup_anchor | 弹出框锚点坐标[x,y] | [number, number] | null | 否 | 必须为包含2个数字的数组 |
| bg_pos | 背景相对位置[x,y](像素) | [number, number] | [0,0] | 否 | 必须为包含2个数字的数组 |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| - | - | - |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| default | 自定义图标内容(仅支持html) |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | - | - | - |


# Image Service

图像服务层，用于通过Web服务提供的栅格数据
## 基础用法


```vue
<template>
  <vl-map :center="[47.655548, -122.303200]" :zoom='12'>
    <template #layers>
      <vl-image-service :url="url" name='image service'
                        :rendering_rule='rendering_rule'
                        format='jpgpng'
                        attribution='USGS, NASA' />
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
url='https://landsat.arcgis.com/arcgis/rest/services/Landsat/PS/ImageServer'
rendering_rule={"rasterFunction":"Pansharpened Enhanced with DRA"}
</script>

```

## API

### 属性

默认情况下，在发起图像服务层请求时，format、band_ids、time、rendering_rule等选项附加到请求URL中。

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 验证规则/备注 |
|--------|------|------|--------|------|--------------|
| url | 图像服务URL | string | '' | 是 | 必须以http/https开头 |
| f | 响应格式 | string | 'image' | 否 | 流式传输使用'image' |
| name | 图层名称 | string | '' | 否 | - |
| format | 图像导出格式 | string | 'jpgpng' | 否 | 支持jpgpng/png/png8/png24/jpg/bmp/gif/tiff/png32/bip/bsq/lerc |
| pixel_type | 栅格数据类型 | string | 'UNKNOWN' | 否 | 支持C128/C64/F32/F64/S16/S32/S8/U1/U16/U2/U32/U4/U8/UNKNOWN |
| no_data | 空值像素值 | Array\<number\> | [] | 否 | - |
| no_data_interpretation | 空值解释方式 | string | '' | 否 | esriNoDataMatchAny/esriNoDataMatchAll |
| interpolation | 像素重采样方法 | string | '' | 否 | RSP_BilinearInterpolation/RSP_CubicConvolution/RSP_Majority/RSP_NearestNeighbor |
| compression_quality | 压缩质量 | number | 100 | 否 | 0-100损失质量 |
| band_ids | 波段ID数组 | Array\<number\> | [] | 否 | 多波段图像使用 |
| time | 时间范围 | Array\<string\> | [] | 否 | 时间过滤条件 |
| rendering_rule | 渲染规则 | Object | {} | 否 | 服务端渲染配置 |
| mosaic_Rule | 镶嵌规则 | Object | {} | 否 | 影像镶嵌配置 |
| endpoint | 服务端点格式 | string | 'Esri' | 否 | 目前仅支持Esri |
| attribution | 数据源属性 | string | '' | 否 | - |
| crs | 坐标参考系统 | string | 'EPSG3857' | 否 | 支持Earth/EPSG3395/EPSG3857/EPSG4326/Base/Simple |
| interactive | 是否交互式 | boolean | false | 否 | 点击事件回调 |
| update_interval | 平移更新间隔(ms) | number | 200 | 否 | 平移时查询更新 |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| click | 点击事件(interactive为true时触发) | {x: number, y: number, latlng: [number,number]} |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| - | - |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | - | - | - |

ref: https://ipyleaflet.readthedocs.io/en/latest/layers/image_service.html


### Aswsome Icon 

## 基础用法

```vue
<template>
  <vl-map :center="p">
    <template #layers>
      <vl-marker :location='p' name='awesome icon'>
        <template #icon>
         <vl-awesome-icon name='bus' marker_color='red' icon_color='black'/>
        </template>
      </vl-marker>
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref

p = [52.204793, 360.121558]

</script>

```

## API

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 备注 |
|--------|------|------|--------|------|------|
| name | FontAwesome图标名称 | string | - | 是 | 参考[FontAwesome 4.7图标库](https://fontawesome.com/v4.7.0/icons)，注意：该组件不支持动态更新 |
| marker_color | 图标背景色 | string | 'blue' | 否 | 使用CSS颜色值 |
| icon_color | 图标颜色 | string | 'white' | 否 | 使用CSS颜色值 |
| spin | 是否旋转图标 | boolean | false | 否 | 启用旋转动画效果 |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| - | - | - |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| - | - |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | - | - | - |


# AntPath

## 基础用法

```vue
<template>
  <Button @click='on_click()'>Switch color</Button>
  <vl-map :center="[51.332, 6.853]" :zoom=10>
    <template #layers>
      <vl-ant-path
        :locations="path"
        :dash_array="[1, 10]"
        :delay="1000"
        :color='color.value',
        pulse_color='#3f6fba'
        name='ant path'
      />
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref

path = [
    [51.185, 6.773], [51.182, 6.752], [51.185, 6.733], [51.194, 6.729],
    [51.205, 6.732], [51.219, 6.723], [51.224, 6.723], [51.227, 6.728],
    [51.228, 6.734], [51.226, 6.742], [51.221, 6.752], [51.221, 6.758],
    [51.224, 6.765], [51.230, 6.768], [51.239, 6.765], [51.246, 6.758],
    [51.252, 6.745], [51.257, 6.724], [51.262, 6.711], [51.271, 6.701],
    [51.276, 6.702], [51.283, 6.710], [51.297, 6.725], [51.304, 6.732],
    [51.312, 6.735], [51.320, 6.734], [51.326, 6.726], [51.334, 6.713],
    [51.340, 6.696], [51.344, 6.678], [51.349, 6.662], [51.354, 6.655],
    [51.360, 6.655], [51.366, 6.662], [51.369, 6.675], [51.373, 6.704],
    [51.376, 6.715], [51.385, 6.732], [51.394, 6.741], [51.402, 6.743],
    [51.411, 6.742], [51.420, 6.733], [51.429, 6.718], [51.439, 6.711],
    [51.448, 6.716], [51.456, 6.724], [51.466, 6.719], [51.469, 6.713],
    [51.470, 6.701], [51.473, 6.686], [51.479, 6.680], [51.484, 6.680],
    [51.489, 6.685], [51.493, 6.700], [51.497, 6.714]
]
color = ref('#7590ba')

def on_click():
    color.value = 'red'
</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 |
|--------|------|------|--------|------|
| locations | ant-path 经过的坐标点 | Array<[lat: number, long: number]> | - | 是 |
| name | 图层名称 | string | '' | 否 |
| use | 路径形状类型 | 'polyline'\|'polygon'\|'rectangle'\|'circle' | 'polyline' | 否 |
| color | 主虚线颜色 | string | '#0000FF' | 否 |
| weight | 路径宽度 | number | 5 | 否 |
| radius | 圆形半径(当use为circle时生效) | number | 10 | 否 |
| dash_array | 动画虚线大小 | string | '10, 20' | 否 |
| delay | 动画延迟时间(毫秒) | number | 400 | 否 |
| paused | 是否暂停动画 | boolean | false | 否 |
| reverse | 是否反向动画 | boolean | false | 否 |
| hardware_accelerated | 是否使用硬件加速 | boolean | false | 否 |
| pulse_color | 次虚线颜色 | string | '#ffffff' | 否 |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| - | - | - |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| popup | 自定义弹出内容 |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | - | - | - |


# Choropleth

Layer showing a Choropleth effect on a GeoJSON structure.
## 基础用法

```vue
<template>
  <vl-map :center="[43, -100]" :zoom=4>
    <template #layers>
      <vl-choropleth name='choropleth' 
                     :geo_data="data" 
                     :choro_data="unemployment"
                     :colormap="linear.YlOrRd_04"
                     border_color="black"
                     :style="style"
      />
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
import json
import pandas as pd
import requests
from branca.colormap import linear

def load_data(url, filename, file_type):
    r = requests.get(url)
    with open(filename, 'w') as f:
        f.write(r.content.decode("utf-8"))
    with open(filename, 'r') as f:
        return file_type(f)

data = load_data(
    'https://raw.githubusercontent.com/jupyter-widgets/ipyleaflet/master/examples/us-states.json',
    'us-states.json',
     json.load)

unemployment = load_data(
    'https://raw.githubusercontent.com/jupyter-widgets/ipyleaflet/master/examples/US_Unemployment_Oct2012.csv',
    'US_Unemployment_Oct2012.csv',
     pd.read_csv)

unemployment =  dict(zip(unemployment['State'].tolist(), unemployment['Unemployment'].tolist()))

style = {'fillOpacity': 0.8, 'dashArray': '5, 5'}

</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 验证规则/备注 |
|--------|------|------|--------|------|--------------|
| geo_data | 应用等值线效果的GeoJSON数据结构 | Object | - | 是 | 必须包含有效的GeoJSON数据 |
| name | 图层名称 | string | '' | 否 | - |
| choro_data | 用于构建等值线效果的数据 | Object | null | 否 | - |
| value_min | 颜色映射的最小数据值 | number | 0 | 否 | - |
| value_max | 颜色映射的最大数据值 | number | 100 | 否 | - |
| colormap | 使用的颜色映射 | string\|Object | 'linear.OrRd_06' | 否 | 支持字符串或对象格式 |
| key_on | 用于颜色映射效果的要素键名 | string | 'id' | 否 | - |
| nan_color | NaN值多边形的填充颜色 | string | 'black' | 否 | 使用CSS颜色值 |
| nan_opacity | NaN值多边形的不透明度 | number | 0.4 | 否 | 0-1之间的值 |
| default_opacity | 有效数据(非NaN值)的不透明度 | number | 1.0 | 否 | 0-1之间的值，自动验证 |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| - | - | - |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| - | - |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | - | - | - |


# WMS Layer

## 基础用法

```vue
<template>
  <vl-map :center="[38.491, -95.712]" :zoom=4 :basemap="basemaps.CartoDB.Positron">
    <template #layers>
      <vl-wms-layer 
        :url="url1" 
        layers='nexrad-n0r-900913' 
        :transparent='True'
        format='image/png'
        name='World Street' @load='on_load'/>
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from ipyleaflet import basemaps

url1 = "http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi"

def on_load(**kwargs):
    print(kwargs) #  {'event': 'load'}
</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 验证规则/备注 |
|--------|------|------|--------|------|--------------|
| url | WMS服务地址 | string | - | 是 | 必须为有效WMS服务URL |
| layers | WMS图层列表(逗号分隔) | string | '' | 是 | 多个图层用逗号分隔 |
| name | 图层名称 | string | '' | 否 | - |
| styles | WMS样式列表(逗号分隔) | string | '' | 否 | 多个样式用逗号分隔 |
| format | 图像格式 | string | 'image/png' | 否 | 透明图层建议使用png |
| transparent | 是否透明 | boolean | true | 否 | - |
| crs | 坐标参考系统 | string | 'EPSG3857' | 否 | 支持'Earth','EPSG3395','EPSG3857','EPSG4326','Base','Simple' |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| load | WMS图层加载完成时触发 | - |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| - | - |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | - | - | - |


ref: https://ipyleaflet.readthedocs.io/en/latest/layers/wms_layer.html


# WKT Layer

WKTLayer is an ipyleaflet class that allows you to visualize a WKT data on the Map.
## 基础用法

```vue
<template>
  <vl-map :center="[42.3152960829043, -71.1031627617667]" :zoom=17>
    <template #layers>
      <vl-wkt-layer :path="path" :hover_style='hover_style' name='wkt file'/>
      <vl-wkt-layer :wkt_string="wkt_string" :hover_style='hover_style' name='wkt str'/>
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
import os
import requests

hover_style = {"fillColor": "red"}
path = "test.wkt"
if not os.path.exists(path):
    url = "https://github.com/jupyter-widgets/ipyleaflet/raw/master/examples/data/test.wkt"
    r = requests.get(url)
    with open(path, "w") as f:
        f.write(r.content.decode("utf-8"))

wkt_string="POLYGON((10.689697265625 -25.0927734375, 34.595947265625 -20.1708984375, 38.814697265625 -35.6396484375, 13.502197265625 -39.1552734375, 10.689697265625 -25.0927734375))"
</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 备注 |
|--------|------|------|--------|------|------|
| path | WKT文件本地路径 | string | "" | 否 | 与wkt_string二选一 |
| wkt_string | WKT格式字符串 | string | "" | 否 | 与path二选一 |
| name | 图层名称 | string | '' | 否 | - |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| - | - | - |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| - | - |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | - | - | - |

ref: https://ipyleaflet.readthedocs.io/en/latest/layers/wkt_layer.html


# Icon

## 基础用法

```vue
<template>
  <vl-map :center="p">
    <template #layers>
      <vl-marker :location='p' :rotation_angle=90 rotation_origin='22px 94px' name='icon'>
        <template #icon>
         <vl-icon icon_url='https://leafletjs.com/examples/custom-icons/leaf-green.png'
                  :icon_size='[38, 95]' :icon_anchor='[22,94]'/>
        </template>
      </vl-marker>
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref

p = [52.204793, 360.121558]

</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 验证规则 |
|--------|------|------|--------|------|----------|
| icon_url | 图标图片URL | string | - | 是 | 必须为有效URL |
| shadow_url | 阴影图片URL | string | null | 否 | 必须为有效URL |
| icon_size | 图标尺寸[宽,高] | [number, number] | null | 否 | 2个数字的数组(像素) |
| shadow_size | 阴影尺寸[宽,高] | [number, number] | null | 否 | 2个数字的数组(像素) |
| icon_anchor | 图标锚点[x,y] | [number, number] | null | 否 | 2个数字的数组(像素) |
| popup_anchor | 弹出框锚点[x,y] | [number, number] | null | 否 | 2个数字的数组(像素) |
| shadow_anchor | 阴影锚点[x,y] | [number, number] | null | 否 | 2个数字的数组(像素) |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| - | - | - |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| - | - |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | - | - | - |


# Heatmap

## 基础用法

```vue
<template>
  <vl-map :center="[0, 0]" :zoom=2>
    <template #layers>
      <vl-heatmap name='heatmap' :locations="heat" :radius="20"/>
    </template>
    <template #controls>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from random import uniform

heat = [[uniform(-80, 80), uniform(-180, 180), uniform(0, 1000)] for i in range(1000)]
</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 | 必填 | 验证规则/备注 |
|--------|------|------|--------|------|--------------|
| locations | 热力图数据点位置数组 | Array<[number, number, number?]> | - | 是 | 每个元素至少包含[纬度,经度]，可选第三参数表示热度值 |
| name | 图层名称 | string | '' | 否 | - |
| blur | 模糊强度 | number | 15 | 否 | 值越大越模糊 |
| radius | 数据点半径 | number | 25 | 否 | 像素单位 |
| gradient | 热力颜色渐变映射 | Object | {0.4:'blue',<br>0.6:'cyan',<br>0.7:'lime',<br>0.8:'yellow',<br>1.0:'red'} | 否 | 键为0-1的比例值，值为CSS颜色 |

### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| - | - | - |

### 插槽

| 插槽名 | 说明 |
|--------|------|
| popup | 自定义弹出窗口内容 |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| - | - | - | - |


# Widget Control

A control that contains any component.

## 基础用法

```vue
<template>
  <vl-map :center="p" :zoom-control='False' ref='m'>
    <template #controls>
      <vl-widget-control position='topright'>
        <HBox>
          <Dropdown v-model=mapname.value :options=maps @change='change_map' />
          <Button @click=clear_layers()>Clear Layers</Button>
          <Button @click=add_marker() icon='map-marker'>+</Button>
        </HBox>
      </vl-widget-control>
    </template>
  </vl-map>
</template>
<script lang='py'>
from ipyleaflet import basemaps
from vuepy import ref

p = [52.204793, 360.121558]
mark_opacity = ref(1.0)
mark_loc = ref(p)
m = ref(None)
maps = list(basemaps.Esri)
mapname = ref(None)

def add_marker():
    m.value.add(Marker(location=p))

def change_map(e):
    esri = basemaps.Esri[e['new']]
    print(esri)
    print('---')
    m.value.basemap = esri

def clear_layers():
    m.value.clear_layers()

</script>

```

## API

### 属性

| 属性名          | 说明                     | 类型                     | 默认值          |
|----------------|------------------------|--------------------------|----------------|
| position       | 控件位置                 | ^[enum]`'topleft'\|'topright'\|'bottomleft'\|'bottomright'` | 'topright'     |
| width          | 控件宽度                 | ^[string]                | '300px'        |
| height         | 控件高度                 | ^[string]                | 'auto'         |
| max_width      | 最大宽度                 | ^[string]                | '100%'         |
| max_height     | 最大高度                 | ^[string]                | '100%'         |
| min_width      | 最小宽度                 | ^[string]                | '0'            |
| min_height     | 最小高度                 | ^[string]                | '0'            |
| margin         | 外边距                   | ^[string]                | '10px'         |
| padding        | 内边距                   | ^[string]                | '10px'         |
| border         | 边框样式                 | ^[string]                | '1px solid #ccc' |
| background     | 背景色                   | ^[string]                | 'white'        |
| border_radius  | 边框圆角                 | ^[string]                | '5px'          |
| box_shadow     | 阴影效果                 | ^[string]                | '0 0 5px rgba(0,0,0,0.2)' |
| z_index        | z-index层级             | ^[number]                | 1000           |
| style          | 自定义CSS样式            | ^[string]                | ''             |

### 事件

| 事件名 | 说明 | 类型 |
|-------|------|------|
| -     | -    | -    |

### 插槽

| 插槽名   | 说明               |
|--------|-------------------|
| default | 控件内部的自定义内容 |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|-------|------|------|--------|
| -     | -    | -    | -      |


# Zoom Control

A control which contains buttons for zooming in/out the Map.
## 基础用法

```vue
<template>
  <vl-map :center="p" :zoom-control='False'>
    <template #controls>
      <vl-zoom-control position='topleft'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref

p = [52.204793, 360.121558]
</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
|--------|------|------|--------|
| position | 控件位置 | ^[enum]`'topleft'\|'topright'\|'bottomleft'\|'bottomright'` | 'topleft' |
| zoom_in_text | 放大按钮文本 | ^[string] | '+' |
| zoom_in_title | 放大按钮标题 | ^[string] | '放大' |
| zoom_out_text | 缩小按钮文本 | ^[string] | '-' |
| zoom_out_title | 缩小按钮标题 | ^[string] | '缩小' |

### Events

| 事件名 | 说明 | 类型 |
|--------|------|------|

### Slots

| 插槽名 | 说明 |
|--------|------|

### 方法

| 方法名 | 说明 | 类型 |
|--------|------|------|


# Search Control

## 基础用法

```vue
<template>
  <vl-map :center="p" :zoom-control='False'>
    <template #controls>
      <vl-search-control 
        url="https://nominatim.openstreetmap.org/search?format=json&q={s}" 
        position="topleft" @location_found=on_loc @feature_found=on_feat
        placeholder='search.'
      >
        <vl-marker v-model="mark_loc.value" name="mark1" @move="on_move" :opacity="mark_opacity.value" title="drag" >
          <template #popup>
            loc: {{ loc_ret.value }}
            feat: {{ feat_ret.value }}
          </template>
        </vl-marker>
      </vl-search-control>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref
from ipyleaflet import basemaps

p = [52.204793, 360.121558]

mark_opacity = ref(1.0)
mark_loc = ref(p)
maps = list(basemaps.Esri)
mapname = ref(None)

loc_ret = ref(None)
feat_ret = ref(None)

def on_loc(**kwargs):
    print('on_loc', kwargs) # {'event': 'locationfound', 'text': '杭州市, 浙江省, 中国', 'feature': None, 'location': [30.2489634, 120.2052342]}
    loc_ret.value = str(kwargs)

def on_feat(**kwargs):
    print('on_feat', kwargs) # {'event': 'locationfound', 'text': '杭州市, 浙江省, 中国', 'feature': None, 'location': [30.2489634, 120.2052342]}
    feat_ret.value = str(kwargs)
    
def on_move(**kwargs):
    print(kwargs)
    print("--")
</script>
</script>

```

## API

### 属性

| 属性名          | 说明                                                                 | 类型                                                                 | 默认值                          |
|----------------|--------------------------------------------------------------------|----------------------------------------------------------------------|---------------------------------|
| position       | 控件位置                                                             | ^[enum]`'topleft' \| 'topright' \| 'bottomleft' \| 'bottomright'`   | 'topleft'                      |
| url            | 用于搜索查询的URL                                                     | ^[string]                                                           | - (必填)                        |
| layer          | 用于搜索查询的图层组                                                   | ^[LayerGroup]                                                       | null                           |
| zoom           | 移动到搜索位置后的缩放级别，默认不改变缩放级别                              | ^[number]                                                           | null                           |
| found_style    | 在图层组中搜索时，搜索到要素的样式                                        | ^[object]                                                           | `{'fillColor': '#3f0', 'color': '#0f0'}` |
| property_name  | 用于显示的属性名称                                                     | ^[string]                                                           | 'display_name'                 |
| auto_complete  | 是否启用自动补全功能                                                   | ^[boolean]                                                          | true                           |

### 事件

| 事件名           | 说明                     | 参数类型 |
|-----------------|------------------------|---------|
| feature_found    | 当要素被找到时触发          | -       |
| location_found   | 当位置被找到时触发          | -       |

### 插槽

| 插槽名    | 说明                  |
|---------|----------------------|
| default | 用于自定义标记(marker)内容 |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|------|-----|------|--------|
| -    | -   | -    | -      |


# Scale Control

A control which shows the Map scale.
## 基础用法

```vue
<template>
  <vl-map :center="p">
    <template #controls>
      <vl-scale-control position='topleft'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref

p = [52.204793, 360.121558]
</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
|--------|------|------|--------|
| position | 控件位置 | ^[enum]`'topleft'\|'topright'\|'bottomleft'\|'bottomright'` | 'bottomleft' |
| max_width | 最大宽度 | ^[number] | 100 |
| metric | 是否使用公制单位 | ^[boolean] | true |
| imperial | 是否使用英制单位 | ^[boolean] | false |

### Events

| 事件名 | 说明 | 类型 |
|--------|------|------|

### Slots

| 插槽名 | 说明 |
|--------|------|

### 方法

| 方法名 | 说明 | 类型 |
|--------|------|------|



# Measure Control

## 基础用法

```vue
<template>
  <vl-map :center="p">
    <template #controls>
      <vl-measure-control position='topleft'></vl-measure-control>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref

p = [52.204793, 360.121558]
</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
|--------|------|------|--------|
| position | 控件位置 | ^[enum]`'topleft'\|'topright'\|'bottomleft'\|'bottomright'` | 'topleft' |
| primary_length_unit | 主要长度单位 | ^[string] | 'meters' |
| secondary_length_unit | 次要长度单位 | ^[string] | 'kilometers' |
| primary_area_unit | 主要面积单位 | ^[string] | 'sqmeters' |
| secondary_area_unit | 次要面积单位 | ^[string] | 'hectares' |
| active_color | 当前测量时的使用的颜色 | ^[string] | '#ABE67E' |
| completed_color | 已完成的测量使用的颜色| ^[string] | '#C8F2BE' |

### Events

| 事件名 | 说明 | 类型 |
|--------|------|------|

### Slots

| 插槽名 | 说明 |
|--------|------|

### 方法

| 方法名 | 说明 | 类型 |
|--------|------|------|



# Geoman Draw Control

GeomanDrawControl allows one to draw various shapes on the map. The drawing functionality on the front-end is provided by [geoman](https://geoman.io/).

The following shapes are supported: - marker - circlemarker - circle - polyline - rectangle - polygon - text

Additionally, there are modes that allow editing of previously drawn shapes:
* edit
* drag
* remove
* cut
* rotate

To have a drawing tool active on the map, pass it a non-empty dictionary with the desired options, see [geoman documentation](https://www.geoman.io/docs/modes/draw-mode#customize-style) for details.
## 基础用法

```vue
<template>
  <vl-map :center="p" :zoom-control='False'>
    <template #controls>
      <vl-geoman-draw-control 
        position='topright' 
        :polyline="polyline" 
        :polygon="polygon" 
        :circlemarker="circlemarker" 
        :rectangle="rectangle" 
      />
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref

p = [52.204793, 360.121558]
polyline = {
    "pathOptions": {
        "color": "red",
        "weight": 8,
        "opacity": 1.0
    }
}

polygon = {
    "pathOptions": {
        "fillColor": "#6be5c3",
        "color": "#6be5c3",
        "fillOpacity": 1.0
    }
}
circlemarker = {
    "pathOptions": {
        "fillColor": "#efed69",
        "color": "#efed69",
        "fillOpacity": 0.62
    }
}
rectangle = {
    "pathOptions": {
        "fillColor": "#fca45d",
        "color": "#fca45d",
        "fillOpacity": 1.0
    }
}
</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
|--------|------|------|--------|
| position | 控件位置 | ^[enum]`'topleft'\|'topright'\|'bottomleft'\|'bottomright'` | 'topleft' |
| draw | 绘制选项 | ^[object] | {} |
| edit | 编辑选项 | ^[object] | {} |

### Events

| 事件名 | 说明 | 类型 |
|--------|------|------|
| draw | 绘制完成时触发 | `(layer: any) => void` |

### Slots

| 插槽名 | 说明 |
|--------|------|

### 方法

| 方法名 | 说明 | 类型 |
|--------|------|------|
|clear_text() | 清除所有文字 ||


# SplitMap Control

## 基础用法

```vue
<template>
  <vl-map :center="p" :zoom='5'>
    <template #controls>
      <vl-split-map-control>
         <template #left>
           <vl-tile-layer :url="url1" name='left'/>
         </template>
         <template #right>
           <vl-tile-layer :url="url2" name='right'/>
         </template>
      </vl-split-map-control>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from ipyleaflet import basemaps

url1 = basemaps.NASAGIBS.ModisTerraTrueColorCR.build_url(time='2017-11-11')
url2 = basemaps.NASAGIBS.ModisAquaBands721CR.build_url(time='2017-11-11')

p = [52.204793, 360.121558]
</script>

```

## API

## API

### 属性

| 属性名          | 说明                     | 类型                     | 默认值      |
|----------------|------------------------|--------------------------|------------|
| position       | 控件位置                 | ^[string]                | 'topleft'  |
| left_layer     | 左侧图层                 | ^[object]                | - (必填)    |
| right_layer    | 右侧图层                 | ^[object]                | - (必填)    |
| direction      | 分割方向                 | ^[string]                | 'vertical' |
| split_position | 分割线位置(百分比)        | ^[number]                | 50         |

### 事件

| 事件名 | 说明 | 类型 |
|-------|------|------|
| -     | -    | -    |

### 插槽

| 插槽名   | 说明               |
|--------|-------------------|
| left   | 左侧图层      |
| right  | 右侧图层      |

### 方法

| 方法名 | 说明 | 参数 | 返回值 |
|-------|------|------|--------|
| -     | -    | -    | -      |


# Fullscreen Control

## 基础用法

```vue
<template>
  <vl-map :center="p">
    <template #controls>
      <vl-fullscreen-control position='topleft'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref

p = [52.204793, 360.121558]
</script>

```

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
|--------|------|------|--------|
| position | 控件位置 | ^[enum]`'topleft'\|'topright'\|'bottomleft'\|'bottomright'` | 'topleft' |
| title | 全屏按钮标题 | ^[string] | '全屏' |
| title_cancel | 全屏退出按钮标题 | ^[string] | '全屏' |

### Events

| 事件名 | 说明 | 类型 |
|--------|------|------|

### Slots

| 插槽名 | 说明 |
|--------|------|

### 方法

| 方法名 | 说明 | 类型 |
|--------|------|------|


# Layers Control

The LayersControl allows one to display a layer selector on the map in order to select which layers to display on the map.

All layers have a name attribute which is displayed in the selector and can be changed by the user.
## 基础用法

```vue
<template>
  <vl-map :center="p" :zoom-control='False'>
    <template #controls>
      <vl-zoom-control position='topleft'/>
      <vl-layers-control position='topleft' :collapsed='False'/>
    </template>
    <template #layers>
      <vl-marker name='mark1' :location='p'/>
      <vl-marker name='mark2' :location='[52.2, 360]'/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref

p = [52.204793, 360.121558]
</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
|--------|------|------|--------|
| position | 控件位置 | ^[enum]`'topleft'\|'topright'\|'bottomleft'\|'bottomright'` | 'topleft' |
| collapsed | 是否折叠 | ^[boolean] | true |

### Events

| 事件名 | 说明 | 类型 |
|--------|------|------|

### Slots

| 插槽名 | 说明 |
|--------|------|

### 方法

| 方法名 | 说明 | 类型 |
|--------|------|------|


# Legend Control

## 基础用法

```vue
<template>
  <Button @click='add()'>Add</Button>
  <vl-map :center="p" :zoom-control='False'>
    <template #controls>
      <vl-legend-control :title="title.value" :legend="dict(legend.value)"/>
      <vl-legend-control :title="title.value" :legend="dict(legend_r)"/>
    </template>
  </vl-map>
</template>
<script lang='py'>
from vuepy import ref, reactive

title = ref('Risk')
legend = ref({"low":"#FAA", "medium":"#A55", "High":"#500"})
legend_r = reactive({"low":"#FAA", "medium":"#A55", "High":"#500"})

def add():
    title.value = 'Risk!'
    legend.value['Higher'] = 'black'
    legend_r['Higher'] = 'black'

p = [52.204793, 360.121558]
</script>

```

## API

### 属性

| 属性名 | 说明 | 类型 | 默认值 |
|--------|------|------|--------|
| position | 控件位置 | ^[enum]`'topleft'\|'topright'\|'bottomleft'\|'bottomright'` | 'topleft' |
| title | 图例标题 | ^[string] | '图例' |
| legend | 图例项, {'name': 'css_color'}形式| ^[dict] | {} |

### Events

| 事件名 | 说明 | 类型 |
|--------|------|------|

### Slots

| 插槽名 | 说明 |
|--------|------|

### 方法

| 方法名 | 说明 | 类型 |
|--------|------|------|

