# VueJS javascript 编程框架

VueJS 是时下最为流行的 Web 前端快速开发框架之一，[中文官网获取更多资源](https://cn.vuejs.org/index.html)

## VueJS 介绍

Vue (读音 /vjuː/，类似于 **view**) 是一套用于构建用户界面的**渐进式框架**。与其它大型框架不同的是，Vue 被设计为可以自底向上逐层应用。Vue 的核心库只关注视图层，不仅易于上手，还便于与第三方库或既有项目整合。另一方面，当与[现代化的工具链](https://cn.vuejs.org/v2/guide/single-file-components.html)以及各种[支持类库](https://github.com/vuejs/awesome-vue#libraries--plugins)结合使用时，Vue 也完全能够为复杂的单页应用提供驱动。

## VueJS 实例

app.js

```javascript
new Vue({
    el:"#vue-app", // Vue作用的根元素，对应div的id属性
    data()=>{
    	name:""
    ｝
});  // 选项
```

index.html

```html
<html>
<head>
    <script "./app.js"></script>
</head>
<body>
   
<div id="vue-app">
    下面为插值表达式，取值于 Vue 实例的 data，渲染到变量的位置
    <h1>
        {{name}}
    </h1>
</div>

{{ name }} // 超出作用范围
    
</body>
</html>
```





## 实例中数据data 和 方法methods

```vue
<script>
    new Vue({
   
    data()=>{
    	name:""
    ｝,
    methods:{
    	greet function(time){
    		return "Good " + time + " " + this.name;
		}
    }
}); 
</script>
```



## 数据绑定

对于网页中便签元素的值可以通过插值表达式赋值，但是对于便签元素自身的属性则需要通过 **v-bind** 对Vue实例的数据绑定了。

```vue
<a v-bind:href="website">The cloudclass website</a><br>
<a :href="website">The cloudclass website</a>
```

>  短格式可以省略 ”v-bind“ 只用一个”：”代表

**v-html** 专门用于直接渲染 HTML 代码，而不会被转义成字符



## 事件

**v-on** 可以实现对 HTML 元素的事件监听和处理。 

```html
<button v-on:click="age++">
    Add a year
</button>
<button v-on:click="age--">
    Subtract a year
</button>
<p>
    My age is {{age}}
</p>
```

> 同样具有着短格式由“@“邮件符号表示  `@click="age++"`



## 事件 modifier



## 键盘事件



## 双向数据绑定

**v-model**

```html
<input type="text" v-model="name">
<span>{{name}}</span>
```



## 计算属性



## 动态CSS

**v-bind:class** 绑定样式**对象**，`true`或者 `false` 代表样式是否启用 

index.html

```html
<div v-bind:class="{available: available}"
```

styles.css

```css
span {
    background: red;
    display: inline-block;
    padding: 10px;
    color: #fff;
    margin: 10px 0;
}

.available span{
    background: green
}
.nearby span:after {
    content:"nearby";
    margin-left: 10px;
}
```

app.js

```javascript
new Vue({
    el: "#vue-app",
    data(){
        available: false,
        nearby： false
    }
});
```



也有另一种用法，同样是对象，可以通过`computed` 计算出样式对象出来，下面给出 javascript 部分的代码

```vue
<script>
new Vue({
    el: "#vue-app",
    data(){
        available: false,
            nearby: false
    },
    methods:{
        
    },
    computed:{
        compClass: function(){
            return {
                avaiable: this.available,
                nearby: this.avaiable
            }
        }
    }
   
})
</script>
```

而在HTML部分中,只需要调用计算的函数，从而做到逻辑与页面展示分离，这样的好处就是不会在HTML页面中掺入太多的javascript语言代码

```vue
<button @click="available = !available">
    Toggle available
</button>
<button @click="nearby = !nearby">
    Toggle nearby
</button>
<div v-bind:class="compClass">
    <span>Ryu</span>
</div>
```



## 条件判断

* **v-if** 成立的条件是其值为 `true`

* **v-else** 

```vue
  <button @click="error = !error">
      Toggle available
  </button>
  <p v-if="error">
      There has been an error
  </p>
  <p v-else>
      Whooo, succeed.
  </p>
```

\ 

* **v-else-if**

* **v-show** 同样可以实现上面的代码效果，它与`v-if`的区别在于，它是使用将HTML元件添加`style="display:none"`来实现展示与否。这一点可以通过浏览器调试工具可以看到。



## v-for 循环

程序语言有条件判断自然少不了循环，**v-for**就是用来处理`VueJS` 中的数组元素的。

先看下面的例子

app.js 中

```vue
new Vue({
    el："#vue-app",
    data(){
    	characters: ["xxx","yyyy","zzzzz"],
        available: true
    }
})
```

在网页中我们固然可以通过插值表达式人工智障的形式一条一条写出来

```vue
<div id="vue-app">
    <h1>
        Looping through lists
    </h1>
    <ul>
        <li>{{characters[0]}}</li>
		<li>{{characters[1]}}</li>
        <li>{{characters[2]}}</li>
    </ul>
</div>
```

> 那要是我们的`characters`数组长度变化不定了？

下面就是解决的方法，那个元素会循环出现，我们就可以在哪里植入`v-for`,这样代码会在渲染到浏览器时转变成以上效果

```vue
<div id="vue-app">
    <h1>
        Looping through lists
    </h1>
    <ul>
        <li v-for="cht in characters">{{cht}}</li>
    </ul>
</div>
```

> **v-for** 的表达式中采用雷同python，shell中的遍历数组 *in* 语法，这时产生新的变量用于循环体中，上面例子中的`cht`,你可以自己随意定义除关键字以外的变量名，之后再在插值表达式中使用。

如果数组中是一系列的对象，只要简单的使用`.`获取对象属性值即可，下面给出另外一个例子

```vue
new Vue({
    data(){
        students:[
            {name:"Joe", age:25, sex:"F"}, 
            {name:"Roy", age:22, sex:"M"},
            {name:"Rose", age:21. sex:"F"}
        ]
    }
})
```

而它的HTML部分可以写成

```html
<div id="vue-app">
    <h1>
        Print every students
    </h1>
    <ul>
       <li v-for="std in students">
        <span>name: {{std.name}}</span>
        <span>age: {{std.age}}</span>
        <span v-if="std.name == 'F' ">She is a girl</span>
        <span v-else>He is a boy</span>
        </li> 
       
    </ul>
</div>
```

> 注意：如果我们的数组提供的元素有着重复的值，VueJS的新版会报错。为了防止这样的现象发生。我们要么提供一个**不同且唯一的**属性作为循环用来区分和识别，或者由循环自己提供一个计数器用来做区分，这就是**v-key**

**v-key** 

VueJS 循环体中提供了一个计数器（从0开始），它是在处理数据时动态递增的，因而对于此循环来说它是唯一的值，

```vue
<li v-for="(std, index) in students" v-key=“index”>
    <span>{{ index }}</span>
    <span>name: {{std.name}}</span>
    <span>age: {{std.age}}</span>
    <span v-if="std.name == 'F' ">She is a girl</span>
    <span v-else>He is a boy</span>
</li>
```

> 提示：在某些场景中，不希望 `v-for`作用在`<div>`元素上，比如排版。这时可以用`<template>`替换掉`<div>`既能够使用循环，又不会渲染出自身的标签元素（不影响循环体中的元素）。	



## Vue组件

为了让代码复用性高，我们可以自己定义组件，在页面中多次调用

通过 **Vue.Component()** 可以实现,第一个参数为新建组件的名字，第二个参数则为一个对象

```vue
Vue.Component('greating', {
    template: '<p>Hey there, I am re-usable component</p>'
})
```

HTML中就可以通过名字作为标签调用

```vue
<div id="vue-app">
    <h2>
        Use component
    </h2>
    <greating></greating>
</div>
```



## $ref



## Vue Cli 命令行

使用命令行可以使用 **webpack** 创建一个开发环境，其好处有：

* 使用 **ES6** 的特性
* 对代码编译可以整合到一个文件中，最终将它压缩化
* 使用单个文件模板
* 在我们机器上事先编译，而不是在客户访问时的浏览器上
* 具有着可以监控代码修改保存而实时重新加载的开发服务



1. 首先我们得安装 chrome v8 javascript 引擎的 node.js ,你可以去[官网下载](http://nodejs.org)最新的版本，安装过程就不在这里介绍了。如果安装完毕，可以检查下对应的版本

```shell
E:\cmder_mini
λ  node -v
   v12.18.3
```

   

2. 接着就可以安装我们的 Vue 特有的 CLI 初始化项目的命令行工具了，[GITHUB项目地址](https://github.com/vuejs/vue-cli)，可以通过`nodejs`中的**npm**命令安装

```shell
npm install -g @vue/cli
```

> 注意：由于CFW问题，使用官网安装javascript开发库可能很慢甚至中断，我们可以设置 npm 使用国内镜像源，这样可以大大提高下载安装的速度
>
```shell
npm config set registry https://registry.npm.taobao.org/
```



3. 在成功安装完**CLI**工具后，我们可以通过 **vue** 命令初始化项目,

```shell
vue init <template-name> <project-folder>
```

```shell
e:\ProjectResources\VueProjects
λ vue init webpack my-project

? Project name my-project
? Project description A Vue.js project
? Author yangwawa0323 <yangwawa0323@163.com>
? Vue build standalone
? Install vue-router? Yes
? Use ESLint to lint your code? Yes
? Pick an ESLint preset Standard
? Set up unit tests No
? Setup e2e tests with Nightwatch? No
? Should we run `npm install` for you after the project has been created? (recommended) npm

   vue-cli · Generated "my-project".
   
Thank you for using core-js ( https://github.com/zloirock/core-js ) for polyfilling JavaScript standard library!

The project needs your help! Please consider supporting of core-js on Open Collective or Patreon:
> https://opencollective.com/core-js
> https://www.patreon.com/zloirock

Also, the author of core-js ( https://github.com/zloirock ) is looking for a good job -)


> ejs@2.7.4 postinstall e:\ProjectResources\VueProjects\my-project\node_modules\ejs
> node ./postinstall.js

Thank you for installing EJS: built with the Jake JavaScript build tool (https://jakejs.com/)


> uglifyjs-webpack-plugin@0.4.6 postinstall e:\ProjectResources\VueProjects\my-project\node_modules\webpack\node_modules\uglifyjs-webpack-plugin
> node lib/post_install.js

npm notice created a lockfile as package-lock.json. You should commit this file.
npm WARN optional SKIPPING OPTIONAL DEPENDENCY: fsevents@1.2.13 (node_modules\webpack-dev-server\node_modules\fsevents):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for fsevents@1.2.13: wanted {"os":"darwin","arch":"any"} (current: {"os":"win32","arch":"x64"})
npm WARN optional SKIPPING OPTIONAL DEPENDENCY: fsevents@1.2.13 (node_modules\watchpack-chokidar2\node_modules\fsevents):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for fsevents@1.2.13: wanted {"os":"darwin","arch":"any"} (current: {"os":"win32","arch":"x64"})
npm WARN optional SKIPPING OPTIONAL DEPENDENCY: fsevents@2.3.2 (node_modules\fsevents):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for fsevents@2.3.2: wanted {"os":"darwin","arch":"any"} (current: {"os":"win32","arch":"x64"})

added 1381 packages from 715 contributors in 237.984s

47 packages are looking for funding
  run `npm fund` for details



Running eslint --fix to comply with chosen preset rules...
# ========================


> my-project@1.0.0 lint e:\ProjectResources\VueProjects\my-project
> eslint --ext .js,.vue src "--fix"


# Project initialization finished!
# ========================

To get started:

  cd my-project
  npm run dev

Documentation can be found at https://vuejs-templates.github.io/webpack
```

以上是交互的提问步骤，详情请见演示，而安装过程则需要等待数分钟。



4. 初始化项目环境后，我们切入到`my-project`目录，然后运行

   ```shell
   λ npm run dev
   
   > my-project@1.0.0 dev e:\ProjectResources\VueProjects\my-project
   > webpack-dev-server --inline --progress --config build/webpack.dev.conf.js
   
    13% building modules 29/31 modules 2 active ...es\VueProjects\my-project\src\App.vue{ parser: "babylon" } is deprecated; we now treat it as { parser: "babel" }.
    95% emitting
   
    DONE  Compiled successfully in 6111ms                                                                      9:14:01 PM
   
    I  Your application is running here: http://localhost:8080
   ```

   这样我们就有了一个测试开发所用的服务，通过浏览器访问本机的8080端口，边开发边调试了。以后再对代码编译发布到真实的服务器上去。

> Vue 还提供了一个图形化初始化的工具,可以通过 **vue ui** 命令实现

* 新版的 Vue CLI 通过简单的 **vue create <project-name>** 创建。

```shell
e:\ProjectResources\VueProjects
λ vue create my-project2


Vue CLI v4.5.11
? Please pick a preset: Default ([Vue 2] babel, eslint)


Vue CLI v4.5.11
✨  Creating project in e:\ProjectResources\VueProjects\my-project2.
�  Initializing git repository...
⚙️  Installing CLI plugins. This might take a while...


> yorkie@2.0.0 install e:\ProjectResources\VueProjects\my-project2\node_modules\yorkie
> node bin/install.js

setting up Git hooks
done


> core-js@3.9.1 postinstall e:\ProjectResources\VueProjects\my-project2\node_modules\core-js
> node -e "try{require('./postinstall')}catch(e){}"


> ejs@2.7.4 postinstall e:\ProjectResources\VueProjects\my-project2\node_modules\ejs
> node ./postinstall.js

added 1258 packages from 947 contributors in 190.841s

69 packages are looking for funding
  run `npm fund` for details

�  Invoking generators...
�  Installing additional dependencies...

added 53 packages from 36 contributors in 23.071s

74 packages are looking for funding
  run `npm fund` for details

⚓  Running completion hooks...

�  Generating README.md...

�  Successfully created project my-project2.
�  Get started with the following commands:

 $ cd my-project2
 $ npm run serve
```



## Vue 项目中的文件和根组件



## 组件嵌套以及导入组件



## 组件的样式







## props 属性

针对每一个子组件修改会影响到所有调用此子组件的其他地方，如果可以从父组件向子组件传递参数，那么将可以很好的避免先前的问题。程序开发过程中，只要在根组件中向所调用到的子组件传递数据，然后子组件获取到数据后再按自己的逻辑展示数据，这样就相当于很好的订制效果。

下面这张图显示了其逻辑

![props属性](VueJS.assets/screenshot-www-bilibili-com-video-BV18U4y1475m-1615909500761%20(1).png)

* 首先在子组件中定义可以识别的参数，这相当于签名，不识别的参数将在控制台出现警告信息

  header.vue

```vue
<template>
	<div>
        <h1>{{ title }}</h1>
    </div>
</template>
<script>
export default {
    props: [ "title" ], // 此处将定义了可以接受的参数列表，
    data: return {
        // title        // 此处的title参数就需要移除，因为title将由父组件调用我的时候，传递给我，见上图
    }
}
</script>
```

而在app.vue中

```vue
<template>
    <div>
    	<app-header v-bind:title="title"></app-header>
    </div>
</template>
<script>
    import Header from './components/Header.vue'
	export default {
        components:{
          'app-header':Header  
        },
        data(){
            title: "Cloudclass vue web demo"
        }
    }
</script>
```

> 注意：父组件要通过 **v-bind** 将属性从自己取出来传递给调用的子组件，遗忘了 **v-bind**， 那么只是将单一的字符串传给了子组件的属性



上面的例子不太严谨，对属性的定义太暧昧，下面给的例子对属性的类型进行了约束

```vue
<script>
	export default {
        props: {
            title:{
                type: String,     // 其他常用的还有 Array，
                required:true
            }
        }
    }
</script>
```

如果传递过来的不是此类型，又或者缺失必要的参数，控制台都会出现`warn`消息。



## 组件的事件处理



## 生命周期钩子 Hook

![Vue 实例生命周期](VueJS.assets/lifecycle.png)

## 插槽 slot



## 动态组件



## 过滤器 Filter



##  表单输入数据的绑定

### 文本框的数据绑定

### 多选框的数据绑定

### 选择框的数据绑定



## HTTP 请求

### GET请求

## 路由

SPA (Single Page Application)为当前时髦的前端技术，比如我们看到的网站，用户点击后很多都只是一小块的地方更新，大体的框架不变，不像以前的网站页面，点击后会出现这个页面的重新加载。这样有两个好处，第一保持了整站的一致性，第二最小化从服务器端获取数据节省用户的流量。

那么问题来了，怎样能做到多页面的效果，还可以回退历史页面了？这个问题就交给我们的 vue-router 来解决，原则上它是 Vue的扩展插件，由于大多数项目都用到它，因为在创建项目中根据提示可以缺省安装，如果没有安装，可以通过下面的命令添加到项目的依赖关系中

```shell
npm install vue-router --save
```

> --save 代表添加到此项目中的依赖关系，别忘了！

### 设置路由

* 接着我们在主程序的入口 **main.js** 中添加并使用 **vue-router**

```vue
<script>
import VueRouter from 'vue-router'

Vue.use(VueRouter)

</script>
```

* 上面的代码中只是引用了 **vue-router** 库，但是具体到如何让路由呈现不同的页面需要初始化一个**路由实例**,这才是关键。实例以一个对象作为参数，参数对应着

  让我们添加一个 src/router.js文件专门存放路由对象, *path*设置路径，*component*为调用对应的组件

  src/router.js

```javascript
import showBlogs from './components/showBlogs.vue';
import addBlog form './components/addBlog.vue'
export default [
    { 
        path:'/',
        component:showBlogs
    },
    {
        path:'/add',
        component: addBlog
    }
]

```

* 在 **main.js** 中引入路由配置

```vue
<script>
import VueRouter from 'vue-router'

Vue.use(VueRouter)
    
// 引入路由到路由实例中    
import Routers from './router.js'    
const router = new VueRouter({
    routers: Routers
})

new Vue({
    el: 'vue-app',
    render: h => h(App),
    router: router  // 将路由实例添加到Vue实例
})

</script>
```

* 一切设置妥当后，那么最后只需要在模板中使用 **router-view** 标签就可以实现 SPA

  app.Vue

```vue
<template>
	<div>
        <router-view></router-view>
    </div>
</template>
```

> 测试时在地址栏输入 http://localhost:8080/**#**/add , 注意它是已一种伪页面跳转的格式，其实都是基于锚点  **#**  后的地址做判断



### 路由的模式 Hash 和 History

### 添加路由链接

### 路由的参数







# Vuetify google 前端 Vue 组件

