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
    try {
        component.createOperations();
    } catch(e) {
        print(e);
    }
}
