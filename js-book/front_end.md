# Element

[参考文档](https://developer.mozilla.org/zh-CN/docs/Web/API/Element)
是 Document 的一个对象。这个接口描述了所有相同种类的元素所普遍具有的方法和属性。例如 HTMLElement 接口是所有 HTML 元素的基础接口，而 SVGElement 是所有 SVG 元素的基本接口。

### 属性

```js
ele.attributes; //返回当前元素的属性
ele.getAttribute('a'); //getter
ele.setAttribute('a', 'b'); //setter
ele.hasAttribute('a'); //判断有没有这个属性
ele.removeAttribute('a'); //移除某个属性
```

```js
var div = document.getElementById('main');
for (var i = 0; i < div.attributes.length; i++) {
  console.log(div.attributes[i].name, div.attributes[i].value);
}
```

### 返回 id 和 class 和 style 和内容

ele.id

ele.classList (数组形式) ["a", "b", "c"]

ele.className (字符串形式) "a b c"

ele.style 元素的 style 属性（返回 CSSStyleDeclaration,一个对象）

ele.innerHTML (字符串形式)

```js
//增加和删除class
ele.classList.add('eee');
ele.className += ' eee';
ele.classList.remove('ever');
```

### 动态创建元素，删除当前元素，复制当前节点

```js
para = document.createElement('p');
document.body.appendChild(para);
document.createTextNode('hello world');
parentEle.insertBefore(newEle, tarEle); //把新元素插到tarEle之前
```

手动写一个 insertAfter

```js
function insertAfter(newEle, tarEle) {
  var parent = tarEle.parentNode;
  if (parent.lastElementChild == tarEle) {
    parent.appendChild(newEle);
  } else {
    parent.insertBefore(newEle, tarEle.nextElementSibling);
  }
}
```

删除元素

```js
ele.remove(); //删除
var oldele = parent.removeChild(ele); //移除子节点，但是仍然在内存中，没有清除
```

深度复制元素

```js
var dupNode = node.cloneNode(); //默认为深度复制
```

### 查找当前元素的儿子,父亲,同胞

```js
firstElementChild  //第一个子元素
lastElementChild   //最后一个子元素
children           //所有子元素的HTMLCollection集合
childElementCount  //子元素个数
next(previous)ElementSibling  //同胞

//下面几个方法返回的包含了非元素节点
firstChild
lastChild
childNodes
next(previous)Sibling

parentNode 爸爸
```

node.nodeType ---- 1:元素节点， 2:属性节点， 3:文本节点
node.nodeName ---- tagName

### disoatchEvent, addEventListener, removeEventListener

手动触发自定义事件,注册事件,移除某个事件

```js
div = document.querySelector('#d');

var fireEvent = function(element, event) {
  if (document.createEventObject) {
    var evt = document.createEventObject();
    return element.fireEvent('on' + event, evt);
  } else {
    var evt = document.createEvent('HTMLEvents');
    evt.initEvent(event, true, true);
    return !element.dispatchEvent(evt);
  }
};
div.addEventListener('ok', function() {
  console.log('ok');
});
fireEvent(div, 'ok');
```

### 共享 onload 事件

```js
function addLoadEvent(func) {
  var oldonload = window.onload;
  if (typeof window.onload != 'function') {
    window.onload = func;
  } else {
    window.onload = function() {
      oldonload();
      func();
    };
  }
}
```

### 查找元素

```js
document.querySelector('div.user-panel.main input[name=login]');
document.getElementById('id1');
document.getElementsByTagName('div');
document.getElementsByClassName('book');
```

### 元素几何特性

```js
var div = document.createElement('div');
document.body.style.margin = '0px';
document.body.style.padding = '0px';
div.style.background = '#ddd';
div.style.height = '300px';
div.style.width = '300px';
div.style.margin = '10px 20px';
div.style.padding = '12px';
div.style.border = '3px solid black';
document.body.appendChild(div);

console.log(div.clientLeft, div.clientTop); //3,3  表示边框宽度
console.log(div.clientHeight, div.clientWidth); //324, 324   content + padding 不包含边框
console.log(div.offsetHeight, div.offsetWidth); //330, 330   content+padding+border
console.log(div.offsetLeft, div.offsetTop); //20, 10         上边距，左边距
console.log(div.scrollHeight, div.scrollWidth); //324, 324  content + padding + 溢出
console.log(div.getBoundingClientRect()); //{top:10, bottom:340, right:350, height:330, left:20, width:330}
```

### 窗口滑动

```js
onscroll = function() {
  //窗口滑动事件
  console.log(document.body.scrollTop); //scrollTop, scrollLeft
};
scrollBy(0, 100); //向下滚动100个像素
scrollTo(0, 500); //滚动到(0,500)
```

# window 对象

navigator: 浏览器对象 navigator.userAgent 用户浏览器判断

screen: 显示器对象 {availWidth: 1920, availHeight: 1053, width: 1920, height: 1080..}

history: 历史对象 back(), forward(), go()

location: 位置对象 hash, host, hostname, href, pathname, port, protocol, search, assign(), reload(), replace()

```js
ele.addEventListener(type, handler, capture);
ele.removeEventListener(type, handler, capture);
ele.preventDefault();
evt.stopPropagation();
```

# XMLHttpRequest

```js
var xhr = new XMLHttpRequest();
xhr.open('get', 'file1.js', true);
xhr.onreadystatechange = function() {
  if (xhr.readyState == 4) {
    if ((xhr.status >= 200 && xhr.status < 300) || xhr.status == 304) {
      var script = document.createElement('script');
      script.type = 'text/javascript';
      script.text = xhr.responseText;
      document.body.appendChild(script);
    }
  }
};
```
