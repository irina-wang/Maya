// File: closestPointOnCurveStrings.cpp
// HEADER FILES:
#include "closestPointOnCurveCmd.h"
#include "closestPointOnCurveNode.h"
#include "closestPointOnCurveStrings.h"
#include <maya/MFnPlugin.h>

// Register all strings used by the plugin C++ source 
static MStatus registerMStringResources(void)
{
      
    MStringResource::registerString(kNoValidObject);
    MStringResource::registerString(kInvalidType);
    MStringResource::registerString(kNoQueryFlag);
    return MS::kSuccess;
}

// INITIALIZES THE PLUGIN BY REGISTERING COMMAND AND NODE:
MStatus initializePlugin(MObject obj)
{
    MStatus status;
    MFnPlugin plugin(obj, PLUGIN_COMPANY, "4.0", "Any");

    // Register string resources used in the code and scripts
    // This is done first, so the strings are available.
    status = plugin.registerUIStrings(registerMStringResources, "closestPointOnCurveInitStrings");
    if (!status)
    {
        status.perror("registerUIStrings");
        return status;
    }
    status = plugin.registerCommand("closestPointOnCurve",  closestPointOnCurveCommand::creator,  closestPointOnCurveCommand::newSyntax);
    if (!status)
    {
        status.perror("registerCommand");
        return status; 
    }
    status = plugin.registerNode("closestPointOnCurve",  closestPointOnCurveNode::id, closestPointOnCurveNode::creator,  closestPointOnCurveNode::initialize);
    if (!status)
    {
        status.perror("registerNode");
        return status;
    }
    return status;
}