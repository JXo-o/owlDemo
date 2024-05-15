import ifcopenshell
import ifcopenshell.geom
import itertools


class IFCParser:

    def __init__(self, ifc_path):
        self.ifc_file = ifcopenshell.open(ifc_path)
        self.settings = ifcopenshell.geom.settings()
        self.element_type_zh = None
        self.element_type = None
        self.elements = None

    def set_element_type(self, element_type_zh, element_type):
        self.element_type_zh = element_type_zh
        self.element_type = element_type
        self.elements = self.ifc_file.by_type(element_type)

    def _get_element_height(self, element):
        try:
            shape = ifcopenshell.geom.create_shape(self.settings, element)
            vert = shape.geometry.verts

            # 将顶点坐标分为三元组
            vertices = list(itertools.zip_longest(*[iter(vert)]*3))

            # 获取所有顶点的Z坐标
            z_coord = [v[2] for v in vertices]

            # 计算最高点和最低点的差值，即为元素高度
            height = max(z_coord) - min(z_coord)
            return height
        except RuntimeError as e:
            print(f"Error processing element ID: {element.GlobalId}, Error: {e}")
            return None

    def process_elements(self, key):
        results = []

        if key == "height":
            for element in self.elements:
                height = self._get_element_height(element)
                if height is not None:
                    results.append(f"{self.element_type_zh}-{element.GlobalId}#{height:.2f}")
                else:
                    print(f"{self.element_type} ID: {element.GlobalId}, Height: Not available")

        return results
