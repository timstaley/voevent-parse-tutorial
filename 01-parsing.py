
# coding: utf-8

# #Parsing VOEvent XML packets with ``voevent-parse``#

# ##Getting started##

# In[ ]:

import voeventparse as vp


# **IPython Tip #1**: In IPython (terminal *or* notebook) you can quickly check the docstring for something by putting a question mark in front, e.g.

# In[ ]:

# Uncomment the following and hit enter:
# ?vp.load


# Alternatively, you can always [read the docs](http://voevent-parse.readthedocs.org), 
# which include autogenerated 
# [API specs](http://voevent-parse.rtfd.org/en/master/reference.html#voeventparse.voevent.load).
# 
# Ok, let's load up a voevent:

# In[ ]:

with open('voevent.xml') as f:
    v = vp.load(f)


# **IPython Tip #2**: We also get tab-completion. Simply start typing the name of a function (or even just the '.' operator) and hit tab to see valid possible options - this is handy for exploring VOEvent packets:

# In[ ]:

# Uncomment the following and hit tab:
# v.


# ##Accessing data##
# 
# ###Text-values###
# 
# 
# **XML Tip #1**: 
# An XML packet is a tree-structure made composed of [elements](http://www.w3schools.com/xml/xml_elements.asp).
# We can dig into the tree structure of the VOEvent, and inspect values:

# In[ ]:

v.Who.Date.text


# In[ ]:

print "Inferred reason is ", v.Why.Inference.Name.text
print "(A string of length", len(v.Why.Inference.Name.text),")"
type(v.Why.Inference.Name.text)


# ###Attributes###
# **XML Tip #2**:
# Note that there are [two ways](http://www.w3schools.com/dtd/dtd_el_vs_attr.asp) to store data in an XML packet: 
# * A single string can be stored as an element's text-value - like the two we just saw.
# * Alternatively, we can attach a number of key-value strings to an element, storing them as [attributes]( http://www.w3schools.com/xml/xml_attributes.asp). We can access these via ``attrib``, which behaves like a Python dictionary, e.g.:

# In[ ]:

print v.attrib['ivorn']
print v.attrib['role']


# In[ ]:

v.Why.Inference.attrib


# ###'Sibling' elements###
# So far, each of the elements we've accessed has been the only one of that name - i.e. our VOEvent has only one ``Who`` child-element, likewise there's only one ``Inference`` under the ``Why`` entry in this particular packet. But that's not always the case; for example the ``What`` section contains a ``Group`` with two child-elements called ``Param``:
# 

# In[ ]:

print vp.prettystr(v.What.Group)


# So how do we access all of these? 
# This is where we start getting into the details of [lxml.objectify syntax](http://lxml.de/objectify.html#the-lxml-objectify-api) (which voevent-parse uses under the hood). 
# **lxml.objectify uses a neat, but occasionally confusing, trick: when we access a child-element by name, what's returned behaves like a list**:

# In[ ]:

v.What[0] # v.What behaves like a list!


# However, to save having to type something like ``v.foo[0].bar[0].baz[0]``, the first element of the list can also be accessed without the ``[0]`` operator (aka ['syntactic sugar'](http://en.wikipedia.org/wiki/Syntactic_sugar)):

# In[ ]:

v.What is v.What[0]


# Knowing that it's 'just a list', we have a couple of options, we can iterate:

# In[ ]:

for par in v.What.Group.Param:
    print par.Description


# Or we can check the length, access elements by index, etc:

# In[ ]:

len(v.What.Group.Param)


# In[ ]:

v.What.Group.Param[1].Description


# Note that another example of this 'syntactic sugar' is that we can display the text-value of an element without adding the ``.text`` suffix. 
# 
# However, see below for why it's a good idea to always use ``.text`` when you really do want the text-value of an element:

# In[ ]:

print v.Why.Inference.Name  # More syntax sugar - if it has a string-value but no children, print the string
print v.Why.Inference.Name.text # The safe option
print v.Why.Inference.Name.text[:3] # Indexing on the string as you'd expect
print v.Why.Inference.Name[:3] # This is indexing on the *list of elements*, not the string!


# If that all sounds awfully messy, help is at hand: you're most likely to encounter sibling elements under the ``What`` entry of a VOEvent, and voevent-parse has a function to convert that to a nested Python dictionary for you:

# In[ ]:

# Consult the docstring
#?vp.pull_params


# In[ ]:

what_dict = vp.pull_params(v)
what_dict


# In[ ]:

what_dict['source_flux']['peak_flux']['value']


# ##Advanced##
# Since voevent-parse uses lxml.objectify, the full power of the LXML library is available when handling VOEvents loaded with voevent-parse. For example, you can find elements using Xpath or [ElementPath](http://lxml.de/tutorial.html#elementpath) queries, but this is beyond the scope of this tutorial: we leave you with just a single example:

# In[ ]:

v.find(".//Param[@name='int_flux']").attrib['value']


# ##Final words##
# Congratulations! You should now be able to extract data from just about any VOEvent packet. 
# Note that voevent-parse comes with a few 
# [convenience routines](http://voevent-parse.readthedocs.org/en/master/reference.html#module-voeventparse.convenience) to help with common, tedious operations, but you can always compose your own. 
# 
# If you put together something that you think others could use (or find a bug!), pull requests are welcome.
# 
# Next stop: authoring your own VOEvent.

# In[ ]:


