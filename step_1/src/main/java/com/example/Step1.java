package com.example;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;

import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.MethodVisitor;
import static org.objectweb.asm.Opcodes.*;
import org.objectweb.asm.Type;

public class Step1 {

  public static void main(String[] args) {

    String stringType = String.class.descriptorString();

    ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_MAXS);
    cw.visit(55, ACC_PUBLIC, "Print", null, Type.getInternalName(Object.class), null);

    MethodVisitor mv = cw.visitMethod(
        ACC_PUBLIC + ACC_STATIC,
        "main",
        "([" + stringType + ")V",
        null, null);

    mv.visitCode();
    mv.visitFieldInsn(GETSTATIC, Type.getInternalName(java.lang.System.class), "out", PrintStream.class.descriptorString());
    mv.visitLdcInsn("Test From Java ASM");
    mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(" + stringType + ")V");
    mv.visitInsn(RETURN);
    mv.visitMaxs(0, 0);
    mv.visitEnd();
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
