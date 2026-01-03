from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass
from typing import List
import sys
from enum import Enum


class OPCODE(Enum):
    # The following is pulled directly from org.objectweb.asm Opcodes.class (v 9.9)
    # The JVM opcode values (with the MethodVisitor method name used to visit them in comment, and
    # where '-' means 'same method name as on the previous line').
    # See https://docs.oracle.com/javase/specs/jvms/se9/html/jvms-6.html.

    NOP = 0  # visitInsn
    ACONST_NULL = 1  # -
    ICONST_M1 = 2  # -
    ICONST_0 = 3  # -
    ICONST_1 = 4  # -
    ICONST_2 = 5  # -
    ICONST_3 = 6  # -
    ICONST_4 = 7  # -
    ICONST_5 = 8  # -
    LCONST_0 = 9  # -
    LCONST_1 = 10  # -
    FCONST_0 = 11  # -
    FCONST_1 = 12  # -
    FCONST_2 = 13  # -
    DCONST_0 = 14  # -
    DCONST_1 = 15  # -
    BIPUSH = 16  # visitIntInsn
    SIPUSH = 17  # -
    LDC = 18  # visitLdcInsn
    ILOAD = 21  # visitVarInsn
    LLOAD = 22  # -
    FLOAD = 23  # -
    DLOAD = 24  # -
    ALOAD = 25  # -
    IALOAD = 46  # visitInsn
    LALOAD = 47  # -
    FALOAD = 48  # -
    DALOAD = 49  # -
    AALOAD = 50  # -
    BALOAD = 51  # -
    CALOAD = 52  # -
    SALOAD = 53  # -
    ISTORE = 54  # visitVarInsn
    LSTORE = 55  # -
    FSTORE = 56  # -
    DSTORE = 57  # -
    ASTORE = 58  # -
    IASTORE = 79  # visitInsn
    LASTORE = 80  # -
    FASTORE = 81  # -
    DASTORE = 82  # -
    AASTORE = 83  # -
    BASTORE = 84  # -
    CASTORE = 85  # -
    SASTORE = 86  # -
    POP = 87  # -
    POP2 = 88  # -
    DUP = 89  # -
    DUP_X1 = 90  # -
    DUP_X2 = 91  # -
    DUP2 = 92  # -
    DUP2_X1 = 93  # -
    DUP2_X2 = 94  # -
    SWAP = 95  # -
    IADD = 96  # -
    LADD = 97  # -
    FADD = 98  # -
    DADD = 99  # -
    ISUB = 100  # -
    LSUB = 101  # -
    FSUB = 102  # -
    DSUB = 103  # -
    IMUL = 104  # -
    LMUL = 105  # -
    FMUL = 106  # -
    DMUL = 107  # -
    IDIV = 108  # -
    LDIV = 109  # -
    FDIV = 110  # -
    DDIV = 111  # -
    IREM = 112  # -
    LREM = 113  # -
    FREM = 114  # -
    DREM = 115  # -
    INEG = 116  # -
    LNEG = 117  # -
    FNEG = 118  # -
    DNEG = 119  # -
    ISHL = 120  # -
    LSHL = 121  # -
    ISHR = 122  # -
    LSHR = 123  # -
    IUSHR = 124  # -
    LUSHR = 125  # -
    IAND = 126  # -
    LAND = 127  # -
    IOR = 128  # -
    LOR = 129  # -
    IXOR = 130  # -
    LXOR = 131  # -
    IINC = 132  # visitIincInsn
    I2L = 133  # visitInsn
    I2F = 134  # -
    I2D = 135  # -
    L2I = 136  # -
    L2F = 137  # -
    L2D = 138  # -
    F2I = 139  # -
    F2L = 140  # -
    F2D = 141  # -
    D2I = 142  # -
    D2L = 143  # -
    D2F = 144  # -
    I2B = 145  # -
    I2C = 146  # -
    I2S = 147  # -
    LCMP = 148  # -
    FCMPL = 149  # -
    FCMPG = 150  # -
    DCMPL = 151  # -
    DCMPG = 152  # -
    IFEQ = 153  # visitJumpInsn
    IFNE = 154  # -
    IFLT = 155  # -
    IFGE = 156  # -
    IFGT = 157  # -
    IFLE = 158  # -
    IF_ICMPEQ = 159  # -
    IF_ICMPNE = 160  # -
    IF_ICMPLT = 161  # -
    IF_ICMPGE = 162  # -
    IF_ICMPGT = 163  # -
    IF_ICMPLE = 164  # -
    IF_ACMPEQ = 165  # -
    IF_ACMPNE = 166  # -
    GOTO = 167  # -
    JSR = 168  # -
    RET = 169  # visitVarInsn
    TABLESWITCH = 170  # visiTableSwitchInsn
    LOOKUPSWITCH = 171  # visitLookupSwitch
    IRETURN = 172  # visitInsn
    LRETURN = 173  # -
    FRETURN = 174  # -
    DRETURN = 175  # -
    ARETURN = 176  # -
    RETURN = 177  # -
    GETSTATIC = 178  # visitFieldInsn
    PUTSTATIC = 179  # -
    GETFIELD = 180  # -
    PUTFIELD = 181  # -
    INVOKEVIRTUAL = 182  # visitMethodInsn
    INVOKESPECIAL = 183  # -
    INVOKESTATIC = 184  # -
    INVOKEINTERFACE = 185  # -
    INVOKEDYNAMIC = 186  # visitInvokeDynamicInsn
    NEW = 187  # visitTypeInsn
    NEWARRAY = 188  # visitIntInsn
    ANEWARRAY = 189  # visitTypeInsn
    ARRAYLENGTH = 190  # visitInsn
    ATHROW = 191  # -
    CHECKCAST = 192  # visitTypeInsn
    INSTANCEOF = 193  # -
    MONITORENTER = 194  # visitInsn
    MONITOREXIT = 195  # -
    MULTIANEWARRAY = 197  # visitMultiANewArrayInsn
    IFNULL = 198  # visitJumpInsn
    IFNONNULL = 199  # -


@dataclass
class Attribute:
    attributeNameIndex: int
    attributeLength: int  # 4 bytes
    info: List[int]


@dataclass
class MethodInfo:
    accessFlags: int
    nameIndex: int
    descriptorIndex: int
    attributesCount: int
    attributeInfo: List[Attribute]  # of size attributesCount


@dataclass
class PoolItem:
    index: int
    value: str | None
    parentRef: List[int] | None


def read_instruction(instruction: int, instructionList: List[int]) -> List[int]:
    count = 0

    if instruction == OPCODE.GETSTATIC.value:
        count = 1

    if instruction == OPCODE.INVOKEVIRTUAL.value:
        count = 1

    if instruction == OPCODE.LDC.value:
        count = 1

    return instructionList[0:count]


def get_next_value(values: List[int]):
    for v in values:
        if v == OPCODE.NOP.value:
            continue
        else:
            return v


def strip_nop(list: List[int]) -> List[int]:
    returnList: List[int] = []
    for i in list:
        if i != 0 and i != 9:
            returnList.append(i)
    return returnList


def get_bytes(data: bytes, index: int, byteCount: int) -> tuple():
    returnBytes = data[index: index+byteCount]
    newPosition = index + byteCount
    return (returnBytes, newPosition)


def get_byte_from_pool(poolIndex: int, data: bytes, index: int) -> tuple():
    poolItem = None
    tagBytes, newPosition = get_bytes(data, index, 1)
    tag = int.from_bytes(tagBytes)

    match tag:
        case 1:  # string
            stringLengthInBytes, newPosition = get_bytes(data, newPosition, 2)
            stringLength = int.from_bytes(stringLengthInBytes, "big")
            returnValue, newPosition = get_bytes(
                data, newPosition, stringLength)
            returnValue = returnValue.decode("utf-8")
            poolItem = PoolItem(poolIndex, returnValue, None)
        case 7:  # class
            classRef, newPosition = get_bytes(data, newPosition, 2)
            returnValue = int.from_bytes(classRef, "big")
            poolItem = PoolItem(poolIndex, None, [returnValue])
        case 8:
            classRef, newPosition = get_bytes(data, newPosition, 2)
            returnValue = int.from_bytes(classRef, "big")
            poolItem = PoolItem(poolIndex, None, [returnValue])
        case 9 | 10 | 11 | 12:  # field | method | interface | Name-Descriptor
            nameIdentifier, newPosition = get_bytes(data, newPosition, 2)
            descriptorIdentifier, newPosition = get_bytes(data, newPosition, 2)
            poolItem = PoolItem(poolIndex, None, [int.from_bytes(
                nameIdentifier, "big"), int.from_bytes(descriptorIdentifier, "big")])
        case _:
            print(f"Can't read tag value {tag}")
            exit(1)

    return (poolItem, newPosition)


def toInt(data: bytes) -> int:
    return int.from_bytes(data, 'big')


def toString(data: bytes) -> str:
    return data.decode("utf-8")


def get_attribute_info(data: bytes, index: int) -> tuple():
    attributeNameIndex, curPosition = get_bytes(data, index, 2)
    attributeLength, curPosition = get_bytes(data, curPosition, 4)

    info, curPosition = get_bytes(
        data, curPosition, int.from_bytes(attributeLength, 'big'))

    return Attribute(toInt(attributeNameIndex),
                     toInt(attributeLength), info), curPosition


def get_method_bytes(data: bytes, index: int) -> tuple():
    attributes: List[Attribute] = []
    accessFlags, curPosition = get_bytes(data, index, 2)
    nameIndex, curPosition = get_bytes(data, curPosition, 2)
    descriptorIndex, curPosition = get_bytes(data, curPosition, 2)
    attributeCount, curPosition = get_bytes(data, curPosition, 2)

    attributeCount = int.from_bytes(attributeCount, 'big')
    for _ in range(attributeCount):
        attr, curPosition = get_attribute_info(data, curPosition)
        attributes.append(attr)

    methodInfo = MethodInfo(toInt(accessFlags), toInt(nameIndex),
                            toInt(descriptorIndex), attributeCount, attributes)

    return methodInfo, curPosition


if len(sys.argv) <= 1:
    print("provide class name")
    exit(1)
data = Path(sys.argv[1]).read_bytes()

curPosition: int = 0
header, curPosition = get_bytes(data, curPosition, 4)
if header != b'\xca\xfe\xba\xbe':
    print("Invalid header")
    exit(1)

minorVersion, curPosition = get_bytes(data, curPosition, 2)
majorVersion, curPosition = get_bytes(data, curPosition, 2)

print(f"Major: {int.from_bytes(majorVersion, 'big')} Minor: {
      int.from_bytes(minorVersion, 'big')}")
poolCount, curPosition = get_bytes(data, curPosition, 2)
print(f"Pool Count: {int.from_bytes(poolCount, 'big')}")

poolCountLength = int.from_bytes(poolCount, 'big')

print("\n")
print("Constant Pool:")

poolItems: List[PoolItem] = []
for i in range(1, poolCountLength):
    value, curPosition = get_byte_from_pool(i, data, curPosition)
    poolItems.append(value)


def resolve_pool_item(index: int, pool: List[PoolItem]):
    resolvedValue = ""

    resolvedItem = next((p for p in pool if p.index == index), None)
    if resolvedItem is not None:
        if resolvedItem.parentRef is not None:
            for parentRef in resolvedItem.parentRef:
                value = resolve_pool_item(parentRef, pool)
                if len(value) > 0:
                    resolvedValue += value

            return f"{resolvedValue}"
        else:
            resolvedValue = resolvedItem.value

    return resolvedValue


for poolItemIndex, poolItem in enumerate(poolItems):
    index = poolItemIndex + 1

    ref = ""
    if poolItem.parentRef:
        ref = "".join(f"#{x}" for x in poolItem.parentRef if len(
            poolItem.parentRef) > 0)
        resolvedItem = "// "
        resolvedItem += resolve_pool_item(index, poolItems)
        print(f"\t{index} {ref:^10}{resolvedItem:>60}")
    else:
        print(f"\t{index} {resolve_pool_item(index, poolItems):^10}")


accessFlags, curPosition = get_bytes(data, curPosition, 2)
# print(f"Access Flags: {int.from_bytes(accessFlags, 'big')}")

thisClassRef, curPosition = get_bytes(data, curPosition, 2)
# print(int.from_bytes(thisClassRef, "big"))
superClassRef, curPosition = get_bytes(data, curPosition, 2)
# print(int.from_bytes(superClassRef, "big"))
interfaceCount, curPosition = get_bytes(data, curPosition, 2)
# print(int.from_bytes(interfaceCount, "big"))

if int.from_bytes(interfaceCount, "big") > 1:
    print("haven't implemented interface counting yet")
    exit(1)

curPosition += 2

fieldCount, curPosition = get_bytes(data, curPosition, 2)
# print(int.from_bytes(fieldCount, "big"))
if int.from_bytes(fieldCount, "big") > 1:
    print("haven't implemented field counting yet")
    exit(1)
curPosition += 2

methodCount, curPosition = get_bytes(data, curPosition, 2)
# print(int.from_bytes(methodCount, "big"))

methodInfo, curPosition = get_method_bytes(data, curPosition)

print(f"\n{methodInfo}")

attributeCount, curPosition = get_bytes(data, curPosition, 2)

attr, curPosition = get_attribute_info(data, curPosition)


instruction = []
currentIndex = 0

strippedList = strip_nop(attr.info)
# print(attr.info)
# print(strippedList)

while True:
    instruction = strippedList[currentIndex]
    currentIndex = currentIndex + 1

    readInstruction = read_instruction(
        instruction, strippedList[currentIndex:])

    if len(readInstruction) == 0:
        currentIndex = currentIndex + 1
        print(f"\t{OPCODE(instruction)}")
    else:
        currentIndex = currentIndex + len(readInstruction)
        instructionAsString = " ".join(f"{x}" for x in readInstruction)
        print(f"\t{OPCODE(instruction)} #{instructionAsString}")

    if instruction == OPCODE.RETURN.value:
        exit(0)
