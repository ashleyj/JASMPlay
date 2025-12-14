package com.example;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;

import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.Label;
import org.objectweb.asm.MethodVisitor;
import static org.objectweb.asm.Opcodes.*;
import org.objectweb.asm.Type;

public class Step4 {

  public static void main(String[] args) {

    ClassWriter mainClass = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
    mainClass.visit(55, ACC_PUBLIC, "Main", null, Type.getInternalName(Object.class), null);

    String stringType = String.class.descriptorString();

    // public static void main(String[] args)
    MethodVisitor mainMethod = mainClass.visitMethod(
        ACC_PUBLIC + ACC_STATIC,
        "main",
        "([" + stringType + ")V",
        null, null);

    mainMethod.visitCode();

    // new Print()
    mainMethod.visitTypeInsn(NEW, "Print");
    mainMethod.visitInsn(DUP);

    // doPrint("Test from Java ASM");
    mainMethod.visitMethodInsn(INVOKESPECIAL, "Print", "<init>", "()V");
    mainMethod.visitVarInsn(ASTORE, 1);
    mainMethod.visitVarInsn(ALOAD, 1);
    mainMethod.visitLdcInsn("Test from Java ASM");
    mainMethod.visitMethodInsn(INVOKEVIRTUAL, "Print", "doPrint", "(" + stringType + ")V");

    mainMethod.visitInsn(RETURN);
    mainMethod.visitMaxs(0, 0);
    mainMethod.visitEnd();

    // end main method
    mainClass.visitEnd();

    // new print class
    ClassWriter printClass = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
    printClass.visit(55, ACC_PUBLIC, "Print", null, Type.getInternalName(Object.class), null);
    
    // constructor public Print() {}
    MethodVisitor constructorMethod = printClass.visitMethod(ACC_PUBLIC, "<init>", "()V", null, null);
    constructorMethod.visitIntInsn(ALOAD, 0);
    constructorMethod.visitMethodInsn(INVOKESPECIAL, Type.getInternalName(Object.class), "<init>", "()V");
    constructorMethod.visitInsn(RETURN);
    constructorMethod.visitMaxs(0, 0);
    constructorMethod.visitEnd();

    // private static void doPrint(String s)
    MethodVisitor doPrintMethod = printClass.visitMethod(ACC_PUBLIC, "doPrint", "(" + stringType + ")V", null, null);

    doPrintMethod.visitFieldInsn(GETSTATIC, Type.getInternalName(java.lang.System.class), "out",
        PrintStream.class.descriptorString());
    doPrintMethod.visitIntInsn(ALOAD, 1);
    doPrintMethod.visitMethodInsn(INVOKEVIRTUAL, Type.getInternalName(PrintStream.class), "println",
        "(" + stringType + ")V");

    doPrintMethod.visitInsn(RETURN);
    doPrintMethod.visitMaxs(0, 0);
    doPrintMethod.visitEnd();

    printClass.visitEnd();

    try {
      writeToFile(mainClass.toByteArray(), "Main.class");
      writeToFile(printClass.toByteArray(), "Print.class");
    } catch (Exception e) {
      e.printStackTrace();
    }

  }

  private static void writeToFile(byte[] bytes, String filename) throws Exception {
    try {
      FileOutputStream stream = new FileOutputStream(filename);
      stream.write(bytes);
      stream.close();
    } catch (IOException e) {
      e.printStackTrace();
    }

  }

}
