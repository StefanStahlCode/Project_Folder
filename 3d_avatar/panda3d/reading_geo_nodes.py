from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, AmbientLight, DirectionalLight, Vec3, Vec4, GeomVertexReader

loadPrcFile("myconfig.prc")

class MainApp(ShowBase):

    def __init__(self):

        super().__init__(self)
        #self.char = self.loader.loadModel("Donut/Donut_1.gltf")
        self.char = self.loader.loadModel("low_poly.glb")
        self.char.setPos(0, 10, -5)
        self.char.reparentTo(self.render)

        # Create a new directional light and set its direction
        dlight = DirectionalLight('dlight')
        dlight.setColor(Vec4(1, 1, 1, 1))
        dlight.setDirection(Vec3(0, 1, 0))

        # Create a NodePath for the light, attach it to the render graph,
        # and call set_light to cause it to cast light on everything in the scene
        dlnp = self.render.attach_new_node(dlight)
        self.render.set_light(dlnp)

        # Add an ambient light
        alight = AmbientLight('alight')
        alight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        alnp = self.render.attach_new_node(alight)
        self.render.set_light(alnp)

        geomNodeCollection = self.char.findAllMatches('**/+GeomNode')
        for nodePath in geomNodeCollection:
            geomNode = nodePath.node()
            self.processGeomNode(geomNode)

    def processGeomNode(self, geomNode):
        for i in range(geomNode.getNumGeoms()):
            geom = geomNode.getGeom(i)
            state = geomNode.getGeomState(i)
            #print(geom)
            #print(state)
            self.processGeom(geom)

    def processGeom(self, geom):
        vdata = geom.getVertexData()
        #print(vdata)
        #self.processVertexData(vdata)
        for i in range(geom.getNumPrimitives()):
            prim = geom.getPrimitive(i)
            print(prim)
            self.processPrimitive(prim, vdata)
        #print(geom.getNumPrimitives(), "primitive")

    def processVertexData(self, vdata):
        vertex = GeomVertexReader(vdata, 'vertex')
        texcoord = GeomVertexReader(vdata, 'texcoord')
        while not vertex.isAtEnd():
            v = vertex.getData3()
            t = texcoord.getData2()
            print("v = %s, t = %s" % (repr(v), repr(t)))

    def processPrimitive(self, prim, vdata):
        vertex = GeomVertexReader(vdata, 'vertex')

        prim = prim.decompose()

        for p in range(prim.getNumPrimitives()):
            s = prim.getPrimitiveStart(p)
            e = prim.getPrimitiveEnd(p)
            for i in range(s, e):
                vi = prim.getVertex(i)
                vertex.setRow(vi)
                v = vertex.getData3()
                print("prim %s has vertex %s: %s" % (p, vi, repr(v)))

def main():
    app = MainApp()
    app.run()

if __name__ == "__main__":
    main()