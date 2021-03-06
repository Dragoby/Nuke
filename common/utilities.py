import nuke
import logging


def allNodes(**kwargs):
    """
    This is an extension on nukes internal node collection and is used to collect all nodes in a script.  This extends
    the ability allowing for re-cursing gizmos

    Kwargs:
        recurseGroups (bool|optional): True or False if the node collection should recurse groups
        recurseGizmos (bool|optional): True or False if the node collection should recurse gizmos
        context (nuke.Node|optional): This is the node context to use when collecting nodes.  Generally used only
                                      when re-cursing gizmos
        nodeClass (str|optional): This is a node class to limit the node collection to

    Returns:
        set: This is a set of all the collected nodes
    """
    recurseGroups = kwargs.get('recurseGroups', False)
    recurseGizmos = kwargs.get('recurseGizmos', False)
    context = kwargs.get('context', None)
    nodeClass = kwargs.get('nodeClass', None)

    if context:
        with context:
            return allNodes(recurseGroups=recurseGroups, recurseGizmos=recurseGizmos)

    if nodeClass:
        baseList = set(nuke.allNodes(nodeClass, recurseGroups=recurseGroups))
    else:
        baseList = set(nuke.allNodes(recurseGroups=recurseGroups))

    if any([recurseGizmos, recurseGroups]):
        for node in baseList:
            if recurseGizmos and isinstance(node, nuke.Gizmo):
                logging.debug('Processing Gizmo:', node.fullName())
                baseList = baseList.union(allNodes(recurseGroups=recurseGroups,
                                          recurseGizmos=recurseGizmos,
                                          context=node))

    return baseList


def select(nodes, **kwargs):
    """
    This will select all of the given nodes,  if the kwarg is passed this will append the current selection.  If append
    is not passed then the current collection will be cleared
    Args:
        nodes (set|nuke.Node|list): This is a set/list of nodes to select or a single node

    Kwargs:
        append (bool): True or False if this should append the current selection of nodes or not
    """
    append = kwargs.get('append', False)
    selected = set()
    if append:
        selected = set(nuke.selectedNodes())

    deselect()

    if isinstance(nodes, nuke.Node):
        nodes = {nodes}
    elif not isinstance(nodes, set):
        nodes = set(nodes)

    nodes = nodes.union(selected)
    for node in nodes:
        node['selected'].setValue(True)


def deselect(nodes=None):
    """
    This will deselect all nodes in the node graph.  If a set/list of nodes are passed then they will be the only nodes
    that are deselected

    Kwargs:
        nodes (set|nuke.Node|list): This is a set/list of nodes to deselect or a single node
    """
    nodes = nodes or allNodes()

    if isinstance(nodes, nuke.Node):
        nodes = {nodes}
    elif not isinstance(nodes, set):
        nodes = set(nodes)

    for node in nodes:
        node['selected'].setValue(False)


def delete(nodes):
    """
    This will delete all of the given nodes,
    Args:
        nodes (set|nuke.Node|list): This is a set/list of nodes to delete or a single node
    """

    if isinstance(nodes, nuke.Node):
        nodes = {nodes}
    elif not isinstance(nodes, set):
        nodes = set(nodes)

    undoStack = nuke.Undo()
    undoStack.begin('Delete Nodes: {0}'.format(len(nodes)))
    for node in nodes:
        nuke.delete(node)
    undoStack.end()
