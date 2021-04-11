# The Complete SASS and SCSS course



## 什么是预处理？

## SASS 与 SCSS

## 安装 SASS

## 快速测试SCSS

## 设置项目的目录结构

## SASS 中变量

### 使用变量

## Partials

```scss
@import "variables"
    
body{
	font-family: $text-font;
    color: $text-color;
}
```



## Mixin

```scss
@mixin warning{
    background-color : orange;
    color: #fff;
}

.warning-button {
    @include warning;
    padding: 8px 12px;
}
```



### 带参数的 Mixin

```scss
@mixin rounded{
    border-radius: 6px;
}
```



```scss
@mixin rounded($radius){
    border-radius: $radius;
}
```



```scss
@mixin rounded($radius: 6px){
    border-radius: $radius;
}
```



如同其他编程语言书写函数遇到的变长长度的参数一样，SCSS也有着自己的变长参数，比如说 **box-shadow** 的阴影效果可以定义多个值，我们在定义 `minix`的时候可以在传入的变量后方加入**三个点**，代表此参数是N个参数一起传入minix

```scss
@mixin box-shadow($shadows...){
    box-shadow:$shadows;
    -moz-box-shadow: $shadows;
    -webkit-box-shadow: $shadows;
}

#header {
    @include box-shadow(2px 0px 4px #999，1px 1px 6px $secondary-color)
    height: $header-height;
    background-color: $theme-color;
}
```



### 传递上下文给 Minix

我们可以由SCSS提供的一个**@content**指令替换我们注入**Minix**的位置对应的内容 

```scss
@mixin apply-to-ie-6 {
    * html {
       @content;
    }
}

@include apply-to-ie-6 {
    body {
        font-size: 125%;
    }
}
```

最终将处理为下面的效果

```css
* html body {
    font-size : 125%;
}
```

> 不要和 Minix 作为函数时混淆，Minix标准使用方法是传入参数，而**@content** 传入的为内嵌进来的样式；