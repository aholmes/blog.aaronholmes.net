
.. meta::
    :date: 2015-01-12

Writing AngularJS directives as TypeScript classes
==================================================

.. pagedate::

Introduction
------------

TL;DR? Read the implementation details here.

**Note:** This post was written for AngularJS 1.x. Angular 2+ has different conventions that make parts of this post obsolete.

`TypeScript <http://www.typescriptlang.org/>`_ is a fantastic language that extends JavaScript by providing static typing syntax. Writing TypeScript to utilize `AngularJS <https://angularjs.org/>`_ can be clunky at times, and one pain point for me was in writing `directives <https://docs.angularjs.org/guide/directive>`_.

AngularJS expects to be `fed <https://docs.angularjs.org/api/ng/provider/$compileProvider#directive>`_ a factory function that returns an object that defines parameters and functionality for your directive.

In JavaScript, that looks like this.

.. code-block:: javascript

    module.directive('myDirective', function()  
    {
        return {
            scope: {},
            template: '<div>{{name}}</div>',
            link: function (scope)
            {
                scope.name = 'Aaron';
            }
        };
    }

A direct translation of this to TypeScript looks like this. By the way, I am using the `angular.d.ts <https://github.com/borisyankov/DefinitelyTyped/blob/master/angularjs/angular.d.ts>`_ type definition file from `definitelytyped.org <http://definitelytyped.org/>`_.

.. code-block:: typescript

    module MyModule.Directives  
    {
        export interface IMyScope extends ng.IScope
        {
            name: string;
        }

        export function MyDirective(): ng.IDirective
        {
            return {
                template: '<div>{{name}}</div>',
                scope : {},
                link  : (scope: IMyScope) =>
                {
                    scope.name = 'Aaron';
                }
            };
        }
    }

The registration is then handled as follows.

``module.directive('projects', MyModule.Directives.MyDirective.Factory());``

Not too different, really, but I feel this doesn't encapsulate a directive very well, nor does it really take advantage of the utility of TypeScript.

Why this is problematic
-----------------------

If ``MyDirective`` is a base class, I would not be able to extend ``MyDirective`` with a subclass. Granted, because TypeScript is a superset of JavaScript, it would be possible to extend this function through prototypal inheritance, or one of a plethora of such approaches. This, however, has the disadvantage of muddying your TypeScript with syntax and code that doesn't necessarily need to be there.

A real-world example without a class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To bring my examples into the real world, here's a previous iteration of a directive I wrote for my personal site. This uses the ``export function`` syntax.

.. code-block:: typescript

    module AaronholmesNet.Directives  
    {
        interface IProject extends Resources.IProject
        {
            title: string;
            active: boolean;
        }

        interface IProjectsScope extends ng.IScope
        {
            [key: string] : any;

            projects: Interfaces.IListInterface<IProject>
        }

        // return my repositories first, and forks second.
        // from there, sort by last change time.
        function ProjectSort(a: Resources.IProject, b: Resources.IProject): number
        {

            if (a.fork === false && b.fork === true) return -1;

            if (a.fork === true && b.fork === false) return 1;

            if (a.updated_at > b.updated_at) return -1;

            if (a.updated_at < b.updated_at) return 1;

            return 0;
        }

        export function ProjectsDirective(ProjectResource: Resources.IProjectResource, $location: ng.ILocationService, $sanitize: ng.sanitize.ISanitizeService, $sce: ng.ISCEService): ng.IDirective
        {
            return {
                templateUrl: '/Views/Home/projects.html',
                scope : {},
                link  : (scope: IProjectsScope) =>
                {
                    var projectMap: { [key: number]: IProject; } = {};

                    scope.projects = [];

                    ProjectResource.query((data: IProject[]) =>
                    {
                        data.sort(ProjectSort);

                        var pathname = $location.path();

                        var activeSet = false;
                        data.forEach((project: IProject) =>
                        {
                            project.active = pathname == '/' + project.id;
                            activeSet = activeSet || project.active;

                            project.name        = $sanitize(project.name);
                            project.description = $sanitize(project.description);
                            project.url         = $sce.trustAsUrl(project.url);
                            project.readme      = $sce.trustAsHtml(project.readme);

                            project.title = project.name + (project.fork ? ' (fork)' : ' (repo)');

                            scope.projects.push(project);

                            projectMap[project.id] = scope.projects[scope.projects.length - 1];
                        });

                        if (!activeSet)
                        {
                            data[0].active = true;
                        }
                    },
                    (data: any) =>
                    {
                        throw new Error(data);
                    });

                    // toggle which tab and tab detail is visible when a link is clicked
                    scope.$on('$locationChangeStart', (event, next, current) =>
                    {
                        var a = <HTMLAnchorElement>document.createElement('A');

                        a.href = current;
                        var pathname = (<string>(a.pathname.match(/^\/(\d+)/) || [,0]))[1];
                        var currentId = pathname == undefined ? 0 : parseInt(pathname, 10);

                        a.href = next;
                        pathname = (<string>(a.pathname.match(/^\/(\d+)/) || [,0]))[1];
                        var nextId = pathname == undefined ? 0 : parseInt(pathname, 10);

                        currentId && (projectMap[currentId].active = false);
                        nextId    && (projectMap[nextId].active    = true);
                    });
                }
            };
        }

        ProjectsDirective['$inject'] = ['ProjectResource', '$location', '$sanitize', '$sce'];
    }


The issues with this approach
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Because the exported function does not utilize a class structure, it's necessary to either use prototypal inheritance or methods exposed in the exported functions scope. ``ProjectSort`` is a function that would be better served as a private method in a class.

* The link method is much larger than it needs to be and could be slimmed down by moving the ``$locationChangeStart`` and ``Query`` handler methods into the outer function scope. However, this becomes cumbersome to manage with many enclosed methods outside of the link function body and when you need to expose variables like scope, and $location. You then have to manage those variables in the outer scope as well.

* Due to the length of ``ProjectsDirective``, the minification-safe list of dependencies (``ProjectsDirective['$inject']``) is quite removed from the function signature. It would be easy to forget to include this, or to update it if your dependencies change.

* I've never been a huge fan of returning an object from a function to define my directive, and I would simply like to avoid it.

What can be done instead
------------------------

Thankfully, it's possible to write directives as a class with a bit of a shift in thinking about how you would organize TypeScript, as opposed to how you would organize JavaScript.

The key point to keep in mind is that AngularJS still expects a function that returns an object. It turns out it's simple and clean to do this with a static ``Factory`` method on your class.

That first example of a TypeScript directive looks like this as a class.

.. code-block:: typescript

    module MyModule.Directives  
    {
        export interface IMyScope extends ng.IScope
        {
            name: string;
        }

        export class MyDirective
        {
            public link: (scope: IMyScope, element: ng.IAugmentedJQuery, attrs: ng.IAttributes) => void;
            public template = '<div>{{name}}</div>';
            public scope = {};

            constructor()
            {
                MyDirective.prototype.link = (scope: IMyScope, element: ng.IAugmentedJQuery, attrs: ng.IAttributes) =>
                {
                    scope.name = 'Aaron';
                };
            }

            public static Factory()
            {
                var directive = () =>
                {
                    return new MyDirective();
                };

                directive['$inject'] = [''];

                return directive;
            }
        }
    }


What this accomplishes
^^^^^^^^^^^^^^^^^^^^^^

* We now have proper properties, fields, and methods on our class instance. ``link``, ``template``, and ``scope`` are exposed in JavaScript as function properties. **If I extend this class, my subclass can override these properties and still utilize the base class functionality**.

* The link method is now another property on the class where its initialization can utilize the class instances scope for property access.

* The factory function is very short, and so the list of dependencies is immediately in front of the developer. While not perfect, it makes it a little more obvious that the directive function and its ``$inject`` property are related.

* This completely avoids having to return an object from a function because your class instance is the object that ``Factory`` returns to angular.

A real-world example with a class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now let's take a look at how I refactored my original ``ProjectsDirective`` to utilize a class structure. You can see here how I take advantage of exposing public properties as the same properties the directive method would normally set in the object it returns. You can also see the private methods and properties I've made available to the class instance in order to avoid relying on function scoping.

.. code-block:: typescript

    module AaronholmesNet.Directives  
    {
        'use strict';

        export interface IProject extends Resources.IProject
        {
            title: string;
            active: boolean;
        }

        export interface IProjectsScope extends ng.IScope
        {
            [key: string] : any;

            projects: Interfaces.IListInterface<IProject>
        }

        export class ProjectsDirective
        {
            // #region Angular directive properties, fields, and methods
            public templateUrl = '/Views/Home/projects.html';
            public scope       = {};
            public link: (scope: IProjectsScope, element: ng.IAugmentedJQuery, attrs: ng.IAttributes) => void;
            // #endregion

            // #region Initialization and destruction
            constructor(ProjectResource: Resources.IProjectResource, $location: ng.ILocationService, $sanitize: ng.sanitize.ISanitizeService, $sce: ng.ISCEService)
            {
                this._$location = $location;
                this._$sanitize = $sanitize;
                this._$sce      = $sce;

                ProjectsDirective.prototype.link = (scope: IProjectsScope, element: ng.IAugmentedJQuery, attrs: ng.IAttributes) =>
                {
                    scope.projects = [];

                    ProjectResource.query(this._handleProjectQuerySuccess.bind(this), this._handleProjectQueryError.bind(this));

                    // toggle which tab and tab detail is visible when a link is clicked
                    scope.$on('$locationChangeStart', this._handleLocationChangeStart.bind(this));

                    scope.$on('$destroy', this.destruct);

                    this._scope = scope;
                }
            }

            public static Factory()
            {
                var directive = (ProjectResource: Resources.IProjectResource, $location: ng.ILocationService, $sanitize: ng.sanitize.ISanitizeService, $sce: ng.ISCEService) =>
                {
                    return new ProjectsDirective(ProjectResource, $location, $sanitize, $sce);
                };

                directive['$inject'] = ['ProjectResource', '$location', '$sanitize', '$sce'];

                return directive;
            }

            private destruct()
            {
                this._projectMap = null;
                this._$location  = null;
                this._$sanitize  = null;
                this._$sce       = null;
                this._scope      = null;
            }
            // #endregion

            // #region Private class properties, fields, and methods
            private _projectMap : { [key: number]: IProject; } = {};
            private _$location  : ng.ILocationService;
            private _$sanitize  : ng.sanitize.ISanitizeService;
            private _$sce       : ng.ISCEService;
            private _scope      : IProjectsScope;
            // #endregion

            // #region Private event handlers
            // return my repositories first, and forks second.
            // from there, sort by last change time.
            private _projectSort(a: Resources.IProject, b: Resources.IProject): number
            {
                if (a.fork === false && b.fork === true) return -1;

                if (a.fork === true && b.fork === false) return 1;

                if (a.updated_at > b.updated_at) return -1;

                if (a.updated_at < b.updated_at) return 1;

                return 0;
            }

            private _handleProjectQuerySuccess(data: IProject[]): void
            {
                data.sort(this._projectSort);

                var pathname = this._$location.path();

                var activeSet = false;
                data.forEach((project: IProject) =>
                {
                    project.active = pathname == '/' + project.id;
                    activeSet      = activeSet || project.active;

                    project.name        = this._$sanitize(project.name);
                    project.description = this._$sanitize(project.description);
                    project.url         = this._$sce.trustAsUrl(project.url);
                    project.readme      = this._$sce.trustAsHtml(project.readme);

                    project.title = project.name + (project.fork ? ' (fork)' : ' (repo)');

                    this._scope.projects.push(project);

                    this._projectMap[project.id] = this._scope.projects[this._scope.projects.length - 1];
                });

                if (!activeSet)
                {
                    data[0].active = true;
                }
            }

            private _handleProjectQueryError(data: any): void
            {
                throw new Error(data);
            }

            private _handleLocationChangeStart(event: ng.IAngularEvent, next: string, current: string): void
            {
                var a = <HTMLAnchorElement>document.createElement('A');

                a.href = current;
                var pathname = (<string[]>(a.pathname.match(/^\/(\d+)/) || [, 0]))[1];
                var currentId = pathname == undefined ? 0 : parseInt(pathname, 10);

                a.href = next;
                pathname = (<string[]>(a.pathname.match(/^\/(\d+)/) || [, 0]))[1];
                var nextId = pathname == undefined ? 0 : parseInt(pathname, 10);

                currentId && (this._projectMap[currentId].active = false);
                nextId && (this._projectMap[nextId].active = true);
            }
            // #endregion
        }
    }


Takeaways and wrap up
---------------------

This approach is not perfect, however I feel it has real strength when focusing heavily on object-oriented programming. I don't demonstrate it here, but the ability to extend base class directives has been very helpful in another project. I also believe the encapsulation is much more clear, and lends itself to avoiding many of the issues we're all familiar with in regards to prototypal inheritance and JavaScript's strange function scoping rules.

Gotchas
^^^^^^^

* It's important to note that you may have to bind contexts for event handlers. For example, with this call ``scope.$on('$locationChangeStart', this._handleLocationChangeStart.bind(this));`` we must bind ``_handleLocationChangeStart`` to the class instance context because scope.$on will call it within the context of ``window``. If someone knows of a way to handle this in TypeScript without ``bbid``, I'd love to hear your input.

* The ``scope`` property is public, and is the same property that is returned from a directive function. ``_scope`` is private and is the actual directive's scope object, not the isolate scope definition.

* It sucks that many parts of the directive function signature are duplicated in the function returned from Factory, the instantiation call, and the constructor signature. I would love to hear alternate ways to accomplish this.

  * `b091 <https://disqus.com/by/bogusawskrzypkowiak/>`_ discovered a way to avoid both the redundancies and the Factory method by using decorators. See `this comment <https://blog.aaronholmes.net/writing-angularjs-directives-as-typescript-classes/#comment-2206875553>`_ for more information.

* It is possible to unintentially create only a single instance of your directive by binding functions and variables in the constructor. For any data members that need to be unique between instances, ensure that they are added to the classes ``prototype`` rather than the instance itself. See `this comment <https://blog.aaronholmes.net/writing-angularjs-directives-as-typescript-classes/#comment-2111298002>`_ for more information.

Back to the basics
^^^^^^^^^^^^^^^^^^

To summarize, here are the basic pieces you need to get this working.

* A static factory method and a constructor.

.. code-block:: typescript

    class MyDirective  
    {
        constructor(/*list of dependencies*/)
        {
        }

        public static Factory()
        {
        }
    }

* A public link method that accepts the same parameters any AngularJS directive accepts, and returns void. Include any other directive properties you need, such as template and scope.

.. code-block:: typescript

    class MyDirective  
    {
        public link: (scope: ng.IScope, element: ng.IAugmentedJQuery, attrs: ng.IAttributes) => void;
        public template = '<div>{{name}}</div>';
        public scope = {};

        constructor(/*list of dependencies*/)
        {
        }

        public static Factory()
        {
        }
    }

* The initialization of the link method.

.. code-block:: typescript

    class MyDirective  
    {
        public link: (scope: ng.IScope, element: ng.IAugmentedJQuery, attrs: ng.IAttributes) => void;
        public template = '<div>{{name}}</div>';
        public scope = {};

        constructor(/*list of dependencies*/)
        {
            // It's important to add `link` to the prototype or you will end up with state issues.
            // See http://blog.aaronholmes.net/writing-angularjs-directives-as-typescript-classes/#comment-2111298002 for more information.
            MyDirective.prototype.link = (scope: ng.IScope, element: ng.IAugmentedJQuery, attrs: ng.IAttributes) =>
            {
                /*handle all your linking requirements here*/
            };
        }

        public static Factory()
        {
        }
    }

  
* The instantiation call from your Factory method.

.. code-block:: typescript

    class MyDirective  
    {
        public link: (scope: ng.IScope, element: ng.IAugmentedJQuery, attrs: ng.IAttributes) => void;
        public template = '<div>{{name}}</div>';
        public scope = {};

        constructor(/*list of dependencies*/)
        {
            // It's important to add `link` to the prototype or you will end up with state issues.
            // See http://blog.aaronholmes.net/writing-angularjs-directives-as-typescript-classes/#comment-2111298002 for more information.
            MyDirective.prototype.link = (scope: ng.IScope, element: ng.IAugmentedJQuery, attrs: ng.IAttributes) =>
            {
                /*handle all your linking requirements here*/
            };
        }

        public static Factory()
        {
            var directive = (/*list of dependencies*/) =>
            {
                return new MyDirective(/*list of dependencies*/);
            };

            directive['$inject'] = ['/*list of dependencies*/'];

            return directive;
        }
    }

* And finally, the registration of your directive with AngularJS by calling the Factory method.

**It's important to note that Factory is executed here, and its returned value (the directive) is passed to Angular's registration function.** :underline:`Be sure to include the parenthesis!`

.. tags:: JavaScript, TypeScript, AngularJS, Directives
