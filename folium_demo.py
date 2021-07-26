from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import sys
import os
import folium
from jinja2 import Template

# 调用高德地图http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}
Map = \
    folium.Map(location=[34.2634, 109.0432],
               zoom_start=16,
               control_scale=True,
               tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
               attr='default')


class MyClickForMarker(folium.ClickForMarker):
    _template = Template(u"""
                {% macro script(this, kwargs) %}
                    function newMarker(e){
                        var new_mark = L.marker().setLatLng(e.latlng).addTo({{this._parent.get_name()}});
                        new_mark.dragging.enable();
                        new_mark.on('dblclick', function(e){ {{this._parent.get_name()}}.removeLayer(e.target)})
                        var lat = e.latlng.lat.toFixed(4),
                           lng = e.latlng.lng.toFixed(4);
                        new_mark.bindPopup({{ this.popup }});
                        };
                    {{this._parent.get_name()}}.on('click', newMarker);
                {% endmacro %}
                """)  # noqa

    def __init__(self, popup=None):
        super(MyClickForMarker, self).__init__()
        self._name = 'ClickForMarker'

        if popup:
            self.popup = ''.join(['"', popup, '"'])
        else:
            self.popup = '"Latitude: " + lat + "<br>Longitude: " + lng '
            print('"Latitude: " + lat + "<br>Longitude: " + lng ')


Map.add_child(folium.LatLngPopup(), name='lng_lat_1')  # 显示鼠标点击点经纬度
# Map.add_child(folium.ClickForMarker(),name='lng_lat_2')  # 将鼠标点击点添加到地图上
Map.add_child(MyClickForMarker(), name='lng_lat_2')  # 将鼠标点击点添加到地图上

# 标记一个实心圆
folium.CircleMarker(
    location=[34.2634, 109.0432],
    radius=3,
    popup='popup',
    color='#DC143C',  # 圈的颜色
    fill=True,
    fill_color='#6495E'  # 填充颜色
).add_to(Map)
Map.save("save_map.html")


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle('地图显示')
        self.resize(1000, 640)
        # 新建一个QWebEngineView()对象
        self.qwebengine = QWebEngineView(self)
        # 设置网页在窗口中显示的位置和大小
        self.qwebengine.setGeometry(20, 20, 960, 600)
        # 在QWebEngineView中加载网址
        path = "file:\\" + os.getcwd() + "\\save_map.html"
        path = path.replace('\\', '/')
        self.qwebengine.load(QUrl(path))
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_lng_lat)
        self.timer.start(1000)

    def show_lng_lat(self):
        print('folium.LatLngPopup()', )

        # "click_for_marker_2f296ff36d3e47b8b77e7c9f1a13edca"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
