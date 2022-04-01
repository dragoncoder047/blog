Title: Why I Prefer Python
Date: 2022-3-30

In developing Phoo today I was unpleasantly presented with yet another reason why I prefer Python. It was when I was working on the new `Importer` API for loading external modules into Phoo that I accidentally did this:

```js
class Importer { /* stub class */ }
class FetchImporter extends Importer {
    constructor(basePath, fetchOptions = {}) {
        /* no super() here */
        this.basePath = basePath;
        this.fetchOptions = fetchOptions;
    }
    /* snip */
}
```

Normally this construct would work in Python as well: A stub base class (which really would be an interface had I written Phoo in Typescript) is then overridden to provide the functionality.

The superclass (`Importer`) has no constructor, so I naturally figured I would not need to call `:::js super()` in the subclass.

Then I got this:

```txt
ReferenceError: Must call super constructor in derived class before accessing 'this' or returning from derived con
structor
```

Well, I'll be! Really?? Python would allow this. I thought Javascript was a duck-typed language which would similarly allow this.

Oh well...
