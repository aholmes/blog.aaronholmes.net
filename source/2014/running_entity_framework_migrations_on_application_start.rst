.. meta::
    :date: 2014-11-28

Running Entity Framework Migrations on Application Start
========================================================

|pagedate|

.. tags:: C#, Entity Framework, ASP.NET, .NET

`Entity Framework <https://www.asp.net/entity-framework>`__ is an ORM developed by Microsoft. It has a useful set of tools and conventions for automatically managing database schema changes called `Code First Migrations <http://msdn.microsoft.com/en-us/data/jj591621.aspx>`__. My only gripe is that, unless you are willing to do some digging, migrations can only be managed with the `PowerShell <http://microsoft.com/powershell>`__ commands ``Add-Migration`` and ``Update-Database``. Even `automatic migrations <http://msdn.microsoft.com/en-us/data/jj554735.aspx>`__ require users to run ``Update-Database``.

There may be many reasons you would want to have migrations automatically run, rather than managing them manually. One reason for me is that I did not want to require that other developers on my team manually run ``Update-Database`` any time there is a database schema change. I feel that it is disruptive to the philosophy of `Getting Shit Done <https://www.amazon.com/Getting-Things-Done-Stress-Free-Productivity/dp/0142000280>`__. On the flip side, not manually managing your databases runs the risk of things breaking and going unnoticed, so use this with care.

Well, I did the digging, and here's what I came up with to run migrations when an ASP.NET website starts.

Update :date:`2014-11-29 <%Y-%m-%d>`
------------------------------------

Somehow I had forgotten that using the database initializer `MigrateDatabaseToLatestVersion <http://msdn.microsoft.com/en-us/library/hh829293%28v=vs.113%29.aspx>`__ is another way to accomplish this. Definitely give it a once over.

----

My ``ApplicationDbContext.cs`` is fairly straightforward.

.. code-block:: csharp
   
    namespace MyNamespace.DAL  
    {
        public class ApplicationDbContext : IdentityDbContext<ApplicationUser>
        {
            public ApplicationDbContext()
                /* This is a static class I use to store environment settings from Web.config. */
                : this(EnvironmentSettings.Current.DatabaseConnections.DatabaseConnectionString())
            {
            }

            public ApplicationDbContext(string connectionString)
                : base(connectionString, throwIfV1Schema: false)
            {
                Configuration.UseDatabaseNullSemantics = true;

    #if DEBUG
                Database.Log = s => System.Diagnostics.Debug.WriteLine(s);
    #endif
            }
        }
    }
    
This is my ``Migrations/Configuration.cs`` file.

.. code-block:: csharp

    namespace MyNamespace.DAL.Migrations  
    {
        public class ConfigurationBase : DbMigrationsConfiguration<ApplicationDbContext>
        {
            public ConfigurationBase()
            {
                AutomaticMigrationsEnabled = false;
                ContextKey = "MyNamespace.DAL.ApplicationDbContext";
            }

            protected void Initialize(string environment = null)
            {
                /*
                    Do some stuff to get your database connection string(s).
                    I store mine in Web.config, and initialize a static class with
                    the values read from that file. This is the same class referenced
                    in my ApplicationDbContext.
                */
            }

            /*
                I use a different class for each environment I need to account for.
                That includes Local, Debug, Stage, and Production.
            */
            public sealed class Local : ConfigurationBase
            {
                public Local()
                    : base()
                {
                    Initialize("local");
                }
            }
        }
    }

And lastly, my ``Startup.cs`` file. This is the important bit.

.. code-block:: csharp

    namespace MyNamespace  
    {
        public partial class Startup
        {
            public void Configuration()
            {
    #if DEBUG
                MigrateDB();
    #endif
            }

            static void MigrateDB()
            {
                var settings = EnvironmentSettings.Current;
                var migratorConfig = new MyNamespace.DAL.Migrations.Local();
                migratorConfig.TargetDatabase = new System.Data.Entity.Infrastructure.DbConnectionInfo(settings.DatabaseConnections.DatabaseConnectionString(), "System.Data.SqlClient");

                var dbMigrator = new DbMigrator(migratorConfig);

                dbMigrator.Update();
            }
        }
    }

Let's break it down a little bit.

First, I only want to run this in my debug environments, so I wrapped the call in a preprocessor block.

.. code-block:: csharp

    #if DEBUG
        MigrateDB();
    #endif

Then I pull my current environment settings from a static class. This class stores my database connection strings. You may need to find another way to pull your database connection strings in.

.. code-block:: csharp
   
    var settings = EnvironmentSettings.Current;  

Armed with our migration configuration class and our connection string, we can instantiate a new "migrator config" and attach a new ``DbConnectionInfo`` instance to it.
Again, ``settings.DatabaseConnections.DatabaseConnectionString()`` comes from my ``EnvironmentSettings`` class, so this will be your own connection string.

You could add some logic here to use different migration configurations instead of just ``Local``.

.. code-block:: csharp

    var migratorConfig = new MyNamespace.DAL.Migrations.Local();  
    migratorConfig.TargetDatabase = new System.Data.Entity.Infrastructure.DbConnectionInfo(settings.DatabaseConnections.DatabaseConnectionString(), "System.Data.SqlClient");  

Finally, we instantiate a ``DbMigrator`` and call ``Update()``.
 
.. code-block:: csharp

    var dbMigrator = new DbMigrator(migratorConfig);  
    dbMigrator.Update();  

|cta|
|disqus|