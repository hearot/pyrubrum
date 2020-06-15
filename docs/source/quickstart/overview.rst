Overview
========

.. figure:: https://a.imgur.com/XhInvbp.gif
    :align: center
    :width: 200px

    An example of what you can build using Pyrubrum.

Menus
-----

Pyrubrum is based on menus and `tree <https://en.wikipedia.org/wiki/Tree_structure>`_ structures, which let the user build a bot in a very simple way.

For example, we want to create a bot that has got a main menu, from which you can access two other menus, one for linking the user to your website and the other one for getting more information about what you do.
The structure is then designed like this:

.. figure:: ../_static/flowcharts/overview.png

This can be effortlessly converted to a Pyrubrum tree:

.. code-block:: python

    from pyrubrum import LinkMenu, Menu

    ...

    {
        Menu("Main menu", "start", "Welcome to my brand new bot."): [
            LinkMenu("Website link", "https://example.com"),
            Menu("About me", "about_me",
                 "My name is John."),
        ]
    }

Intuitive, isn't it?

You may have noticed it actually isn't a tree, as the main menu is within a set as well. The fact is that Pyrubrum does actually work with `forest <https://magoosh.com/data-science/what-is-forest-data-structure/>`_ structures, which are just a collection of multiple trees.
That means you can define multiple :term:`top-level menus <Top-level menu>`!

Let's say we want to create two :term:`top-level menus <Top-level menu>`: we already defined one of them before and we now decide to create a new one for contacting you.

Then the structure has changed to this:

.. figure:: ../_static/flowcharts/overview-1.png

Which translates to:

.. code-block:: python

    from pyrubrum import LinkMenu, Menu

    ...

    {
        Menu("Main menu", "start", "Welcome to my brand new bot."): [
            LinkMenu("Website link", "https://example.com"),
            Menu("About me", "about_me",
                 "My name is John."),
        ],
        Menu("Contact me", "contact", "Email me at me@example.com"): [],
    }
