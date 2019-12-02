# 根据人脸关键点计算欧拉角

## 计划周期36小时

## 内容步骤

1. 读取 特征点信息 
2. 计算 左、右眼睁闭眼状态  （简单）
3. 计算 平面内旋转角ROW[-180(逆时针), 180(顺时针)] （一般）
4. 计算 三维旋转之左右旋转角YAW[-90(左), 90(右)]  （难）
5. 计算 三维旋转之俯仰角度ROLL[-90(上), 90(下)]   （难）

## 验收标准

角度对比可以参考[baidu](https://ai.baidu.com/tech/face/detect)或者[face++](https://www.faceplusplus.com.cn/attributes/)中的angle,误差5°以内即可，或者介于二者之间。提供face++的调用代码

功能封装成函数接口,不考虑文件读取时间,单张数据的计算时间不超过20ms

python,c++ 均可 


## 输入

1. *jpg       人脸图片 
2. *.jpg.txt  人脸特征点

## 输出

1. left_eye_status : boolean 
2. right_eye_status : boolean
3. angle_row : float
4. angle_yaw : float
5. angle_roll : float
   
## 文件结构说明

    Test 
      --new_crop
        --000001.jpg      人脸图片
        ...
      --new_landmark
        --000001.jpg.txt  记录了对应人脸的150个特征点，位置已经根据图片大小进行归一化。
        ...

    show_landmark.py  显示人脸特征点位置的脚本 python show_landmark.py  即可运行

    kuangshi_api.py   得到face++计算出人脸的angle，可作为角度参考 python kuangshi_api.py 既可运行
## Tip

    可以从150特征点选取部分有效的关键点然后去计算，简易版即可
    关键词搜索：人脸姿态估计，头部姿态估计