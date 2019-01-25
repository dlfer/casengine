layout: page
title: test page in markdown
permalink: /latex/
---

## title header 


A link to [Jekyll Now](http://github.com/barryclark/jekyll-now/). A big ass literal link <http://github.com/barryclark/jekyll-now/>
  
  An image, located within /images

  ![an image alt text]({{ site.baseurl }}/images/jekyll-logo.png "an image title")

  * A bulletted list
  - alternative syntax 1
  + alternative syntax 2
    - an indented list item

    1. An
    2. ordered
    3. list

    Inline markup styles: 

    - _italics_
    - **bold**
    - `code()` 

> Blockquote
>> Nested Blockquote 
 
Syntax highlighting can be used by wrapping your code in a liquid tag like so:

{{ "{% highlight javascript " }}%}  
/* Some pointless Javascript */
var rawr = ["r", "a", "w", "r"];
{{ "{% endhighlight " }}%}  

creates...

{% highlight javascript %}
/* Some pointless Javascript */
var rawr = ["r", "a", "w", "r"];
{% endhighlight %}
 
Use two trailing spaces  
on the right  
to create linebreak tags  
 
Finally, horizontal lines
 
----

