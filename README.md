# *Classy*FD

*Classy*FD is a Python library that makes working with files and directories
quick and easy. For example, rather than using many functions that are
scattered throughout different modules, *Classy*FD provides custom classes that
group together (or encapsulate) the data and behavior of objects that represent
real files and directories. Additionally, *Classy*FD provides sane and sensible 
defaults on its provided file and directory operations.

*Classy*FD is written in pure Python, and its only dependency is the Python 
Standard Library.

### Examples

```python
>>> from classyfd import File
>>> 
>>> # Create a File object (absolute and relative paths are supported)
>>> f = File("hello-world.txt")
>>> # The owner of the file
>>> f.owner["username"]
'sizzlingvortex'
>>> # The full, absolute path
>>> f.path
'/home/sizzlingvortex/Development/open-source/python/ClassyFD/hello-world.txt'
>>> # The directory the file is in
>>> f.parent
'/home/sizzlingvortex/Development/open-source/python/ClassyFD'
>>> # The size in bytes
>>> f.size
28
>>> # Rename the file (required to stay in the same directory)
>>> f.rename("whats-up-world.txt")
>>> f.path
'/home/sizzlingvortex/Development/open-source/python/ClassyFD/whats-up-world.txt'
>>> # Move the file
>>> f.move("/home/sizzlingvortex/Desktop/")
>>> f.path
'/home/sizzlingvortex/Desktop/whats-up-world.txt'

```

---
### Status: Work-in-Progress

*Classy*FD is still very much a work-in-progress and, although contains many automated tests to make the code robust, is not recommended for production (yet) due to the possibility of breaking changes in the API. However, production releases are planned once the API becomes more stable and when the official documentation is created.

---

### Supported Versions of Python:
Python 3.4.x (and higher)

### Copyright
Copyright 2016 by Joshua Goring

### License
MIT, see [LICENSE](https://github.com/SizzlingVortex/classyfd/blob/master/LICENSE) for more details.
