=================================================
快速开始
=================================================

1.安装PyGeoC
-------------------------------------------------

PyGeoC处在不断开发完善中，请根据如下命令安装最新开发版本。

.. code-block:: Bash
   :linenos:

   git clone https://github.com/lreis2415/PyGeoC
   cd PyGeoC
   python setup.py install


2.读取栅格文件
-------------------------------------------------
:func:`pygeoc.raster.RasterUtilClass.read_raster` 函数读取栅格数据，
并返回
:class:`pygeoc.raster.Raster` 类的实例，通过其属性和方法可以获取
栅格元数据信息及栅格值的基本统计（如最大值、最小值、平均值、标准差等）。

.. literalinclude:: ../examples/ex01_begin_with_pygeoc.py
   :language: Python
   :linenos:

3.调用TauDEM
-------------------------------------------------
:mod:`pygeoc.TauDEM` 子模块对TauDEM的函数调用进行了封装，以填洼算法（
:func:`pygeoc.TauDEM.TauDEM.pitremove`）为例。

注意：此时mpiexec和pitremove程序的路径均已在环境变量里设置。

此外，该函数允许指定mpiexec和pitremove以及用于多节点并行计算的
hostfile文件的绝对路径。

.. literalinclude:: ../examples/ex02_taudem_simple_usage.py
   :language: Python
   :linenos:

4.子流域划分
-------------------------------------------------
子流域划分是GIS分析中常用的工作流，PyGeoC提供了一种简单的方式完成该任务：
只需提供研究区DEM。同时，该工作流允许用户提供流域出口点数据、河网划分阈值
等参数。用户可根据默认参数下得到的流域划分结果进一步调整参数以达到满意的
流域划分。

* 如未提供流域出口，则该研究区汇流累积量最大的位置默认为流域出口
* 如未提供河网划分阈值，则根据 :func:`pygeoc.TauDEM.TauDEM.dropanalysis` 程序自动确定阈值

.. literalinclude:: ../examples/ex04_watershed_delineation.py
   :language: Python
   :linenos:

5.常用函数积累
-------------------------------------------------
:mod:`pygeoc.utils` 子模块提供了一系列通用函数，如
文件操作类
:class:`pygeoc.utils.FileClass` 、
字符串操作类
:class:`pygeoc.utils.StringClass` 、
时间操作类
:class:`pygeoc.utils.DateClass` 、
常用数学函数类
:class:`pygeoc.utils.MathClass` 、
和其他通用函数类
:class:`pygeoc.utils.UtilClass` 等。

以数学函数类中计算模型模拟Nash-Sutcliffe效率系数（NSE）等指标为例，
下图为实测值和模拟值的散点图分布。

.. plot:: ../examples/ex05_plot_obs_sim.py

模型模拟效率指标计算代码如下：

.. literalinclude:: ../examples/ex06_model_performace_index.py
   :language: Python
   :linenos:
