gitviewfs
========
Gitviewfs provides a filesystem view of a Git repository. It is implemented on
top of [FUSE](http://fuse.sourceforge.net/) with python-fuse. It can be used
to help understand [Git internals](http://git-scm.com/book/en/Git-Internals-Git-Objects),
to debug some problem on your repository or simply as an alternative way of
browsing branches, tags, commits, directories and files in your repository.


How to Use It
===========
This was tested on a Linux Mint 13 64-bit and should work the same way on other
up-to-date Debian-based distros.

* First you need to install python-fuse:
``` shell
sudo apt-get install python-fuse
```

* Choose your `<MOUNTPOINT>` directory and make sure it is empty.
* Then run gitviewfs to mount the filesystem:
``` shell
<PATH-TO-GITVIEWFS>/gitviewfs.py <MOUNTPOINT> -o repo=<GIT-REPOSITORY>
```
Since it uses FUSE, you don't need `root` privileges to mount the filesystem.

* `cd` into `<MOUNTPOINT>` and browse its file hierarchy.


When you are done, umount the filesystem with:
``` shell
fusermount -u <MOUNTPOINT>
```


The Filesystem Hierarchy
=====================
The items bellow describe what you will find under the mountpoint after mounting
the filesystem. The main idea is that references from a Git object to another
object are viewed as symlinks.
* `/refs/HEAD` - a symlink pointing to a branch in `/refs/branches/` according to
the current branch in your repository.
* `/refs/branches/` - a directory that lists the local branches in your repository.
* `/refs/branches/<BRANCH>` - a symlink pointing to the corresponding commit (in
  `/objects/commits/`) which is the current state of the branch.
* `/objects/commits/<COMMIT-SHA1>/` - a directory containing information regarding
 a commit.
* `/objects/commits/<COMMIT-SHA1>/message` - a file containing the commit message.
* `/objects/commits/<COMMIT-SHA1>/author/` - a directory with files containing the
  name, email and date of the commit author.
* `/objects/commits/<COMMIT-SHA1>/committer/` - a directory with files containing
  the name, email and date of the commit committer.
* `/objects/commits/<COMMIT-SHA1>/parents/` - a directory with symlinks that point
  to the commits in `/objects/commits/` which are parents of this commit.
* `/objects/commits/<COMMIT-SHA1>/tree` - a symlink which points to the root directory
  (in `/objects/trees/`) of this commit.
* `/objects/trees/<TREE-SHA1>/`- a directory that represents a directory that 
  was committed. Each item is a symlink that points to either a blob in
  `/objects/blobs/` (when the item is a committed symlink or regular file) or to
  another tree in `/objects/tree/` (when the item is a committed sub-directory).
* `/objects/blobs/<BLOB-SHA1>` - a file whose content is the content of a
  regular file that was committed or the target of a symlink that was committed.


### Limitations
* It provides a **read-only view** of a Git repository.
* It currently does not tell you if a blob referenced by a tree is a regular
  file or a symlink (how can this be implemented?).
* The directories `/objects/commits/`, `/objects/tags/`, `/objects/trees/`,
  `/objects/blobs/`  and `/objects/all/`, **cannot** be used to **list** items.
* Non-"standard" references are not listed. I.e., references which are not HEAD,
  local branches, remote branches or lightweight tags are not listed.


### Implementation Pending
* Should check if repo argument is really a Git repository
* Branches with "/" in name
* Bare repository (has refs/HEAD?)
* Detached-head (refs/HEAD?)
* Repository initialized but without any commit yet (refs/HEAD? refs/commits/?)
* Lightweight tags
* Annotated tags
* Tags with "/" in name
* Directory /objects/all
* Tags pointing to an object which is not a commit
* Handle errors:
	* ls MOUNT-POINT/objects/trees
	* ls MOUNT-POINT/objects/commits
	* ls MOUNT-POINT/objects/blobs
	* ls MOUNT-POINT/objects/tags
	* ...
* Handle conflicting names
	* branch x tag
	* branch x sha1
	* tag x sha1
	* ...
* Handle commit without parents

