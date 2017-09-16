=================================================
API 参考
=================================================
PyGeoC采用 `Google code docstrings <http://google.github.io/styleguide/pyguide.html>`_ 注释风格。该文档由Sphinx从源码中自动提取生成。

子模块
-------------------------------------------------

.. toctree::
   :maxdepth: 2

   pygeoc.utils
   pygeoc.raster
   pygeoc.hydro
   pygeoc.TauDEM
   pygeoc.postTauDEM
   pygeoc.vector


全局变量
-------------------------------------------------
* 数值常量

  * 根号2: 1.4142135623730951
  .. py:data:: pygeoc.utils.SQ2
  * :math:`\pi` : 3.141592653589793
  .. py:data:: pygeoc.utils.PI
  * 零值: 1e-12
  .. py:data:: pygeoc.utils.ZERO
  * 浮点数相等判断: 1e-6
  .. py:data:: pygeoc.utils.DELTA
  * 默认NoData值: -9999.
  .. py:data:: pygeoc.utils.DEFAULT_NODATA

* GDAL数据类型：

.. py:data:: pygeoc.raster.GDALDataType

+--------------+----------------+---------------------------------+
| GDAL数据类型 | GDAL数据类型   | 描述                            |
+==============+================+=================================+
| 0            | GDT_Unknown    | Unknown or unspecified type     |
+--------------+----------------+---------------------------------+
| 1            | GDT_Byte       | Eight bit unsigned integer      |
+--------------+----------------+---------------------------------+
| 2            | GDT_UInt16     | Sixteen bit unsigned integer    |
+--------------+----------------+---------------------------------+
| 3            | GDT_Int16      | Sixteen bit signed integer      |
+--------------+----------------+---------------------------------+
| 4            | GDT_UInt32     | Thirty two bit unsigned integer |
+--------------+----------------+---------------------------------+
| 5            | GDT_Int32      | Thirty two bit signed integer   |
+--------------+----------------+---------------------------------+
| 6            | GDT_Float32    | Thirty two bit floating point   |
+--------------+----------------+---------------------------------+
| 7            | GDT_Float64    | Sixty four bit floating point   |
+--------------+----------------+---------------------------------+
| 8            | GDT_CInt16     | Complex Int16                   |
+--------------+----------------+---------------------------------+
| 9            | GDT_CInt32     | Complex Int32                   |
+--------------+----------------+---------------------------------+
| 10           | GDT_CFloat32   | Complex Float32                 |
+--------------+----------------+---------------------------------+
| 11           | GDT_CFloat64   | Complex Float64                 |
+--------------+----------------+---------------------------------+
