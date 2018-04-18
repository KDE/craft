function Component()
{
    //constructor
}
Component.prototype.isDefault = function()
{
    return true;
}
Component.prototype.createOperations = function()
{
    if (installer.value("os") === "win") {
        @{SHORTCUTS}
    }
    try {
        component.createOperations();
    } catch(e) {
        print(e);
    }
}
