# VFL: Variable-based fault localization
> 基于变量的错误定位技术

## 来源

* 这是复现了论文<VFL: Variable-based fault localization>的一个实验，该论文详见[这里](https://www.researchgate.net/publication/329314758_VFL_Variable-based_Fault_Localization)

* 简单思路是在SBFL的基础上加上变量的覆盖信息，二者加权排序后得到语句的怀疑度列表

## 需求

* 需要`pycparser`这个包来为c/c++解析语法树

* 需要`gcov`来获取c/c++的覆盖信息

## 使用

* VFL文件中调用`get_cpp_VFL_rank()`方法获取c++文件怀疑度列表，调用`get_py_VFL_rank()`方法获取py文件怀疑度列表
