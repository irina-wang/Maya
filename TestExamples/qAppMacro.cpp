QCoreApplication*  app = qApp;
if (app) {
    cout << "Application name is '" << app->applicationName().toStdString() << "'" << endl;
}
