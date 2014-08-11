crack.nc.hust
=============

华科校园网用户名密码破解脚本
----------------------
由于部分密码默认为生日，生成生日字典暴力破解，你可以根据自己的需要采用自己的字典。
P.S. 严重申明，该脚本不能用于邪恶目的。

###Usage:
![usage](screenshot/1.png)

<pre>
	python nc.hust.crack.py -y 2012 -c 10216
</pre>
![ex1](screenshot/2.png)

<pre>
	python nc.hust.crack.py -y 2012 -r 10307 10310
</pre>
![ex2](screenshot/3.png)

###待完成
![tobedone](screenshot/4.png)
获取用户信息，由于登录页面有验证码，下一步完成识别验证码的功能。
