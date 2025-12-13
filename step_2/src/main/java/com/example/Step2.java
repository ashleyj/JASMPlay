package com.example;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;

import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.MethodVisitor;
import static org.objectweb.asm.Opcodes.*;
import org.objectweb.asm.Type;

public class Step2 {

  public static void main(String[] args) {

    ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_MAXS);
    cw.visit(55, ACC_PUBLIC, "Print", null, Type.getInternalName(Object.class), null);

    String stringType = String.class.descriptorString();

    // public static void main(String[] args)
    MethodVisitor mainMethod = cw.visitMethod(
        ACC_PUBLIC + ACC_STATIC,
        "main",
        "([" + stringType + ")V",
        null, null);

    mainMethod.visitCode();
    mainMethod.visitLdcInsn("Test From Java ASM");

    //doPrint(String s)
    mainMethod.visitMethodInsn(INVOKESTATIC, "Print", "doPrint", "(" + stringType + ")V");
    mainMethod.visitInsn(RETURN);
    mainMethod.visitMaxs(0, 0);
    mainMethod.visitEnd();

    // end main method

    // private static void doPrint(String s)
    MethodVisitor doPrintMethod = cw.visitMethod(ACC_PRIVATE + ACC_STATIC, "doPrint", "(" + stringType + ")V", null, null );

    doPrintMethod.visitFieldInsn(GETSTATIC, Type.getInternalName(java.lang.System.class), "out", PrintStream.class.descriptorString());
    doPrintMethod.visitIntInsn(ALOAD, 0);
    doPrintMethod.visitMethodInsn(INVOKEVIRTUAL, Type.getInternalName(PrintStream.class), "println", "(" + stringType + ")V");
    doPrintMethod.visitInsn(RETURN);
    doPrintMethod.visitMaxs(0, 0);
    doPrintMethod.visitEnd();

    cw.visitEnd();

    byte[] bytes = cw.toByteArray();
    try {
      FileOutputStream stream = new FileOutputStream("Print.class");
      stream.write(bytes);
      stream.close();
    } catch (IOException e) {
      e.printStackTrace();
    }

  }

}
