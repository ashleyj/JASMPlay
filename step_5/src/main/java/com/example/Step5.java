package com.example;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;

import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.MethodVisitor;
import org.objectweb.asm.Handle;
import org.objectweb.asm.Label;
import static org.objectweb.asm.Opcodes.*;
import org.objectweb.asm.Type;

public class Step5 {

  public static void main(String[] args) {

    ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
    cw.visit(55, ACC_PUBLIC, "Print", null, Type.getInternalName(Object.class), null);

    String stringType = String.class.descriptorString();
    Label loop = new Label();
    Label end = new Label();

    //dynamic method handle
    Handle methodHandle = new Handle(H_INVOKESTATIC,  "java/lang/invoke/StringConcatFactory","makeConcatWithConstants", "(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;", false);

    // public static void main(String[] args)
    MethodVisitor mainMethod = cw.visitMethod(
        ACC_PUBLIC + ACC_STATIC,
        "main",
        "([" + stringType + ")V",
        null, null);

    mainMethod.visitCode();

    // max counter
    mainMethod.visitLdcInsn(3);
    mainMethod.visitVarInsn(ISTORE, 1);

    // counter
    mainMethod.visitLdcInsn(0);
    mainMethod.visitVarInsn(ISTORE, 2);


    mainMethod.visitLabel(loop);
    mainMethod.visitVarInsn(ILOAD, 2);
    mainMethod.visitVarInsn(ILOAD, 1);

    mainMethod.visitJumpInsn(IF_ICMPGE, end); 
    mainMethod.visitLdcInsn("Print Count From Java ASM: ");
    mainMethod.visitVarInsn(ILOAD, 2);

    // call dynamic concat
    mainMethod.visitInvokeDynamicInsn("makeConcat()", "(" + stringType + "I)" + stringType, methodHandle, "\u0001 \u0001");

    //doPrint(String s)
    mainMethod.visitMethodInsn(INVOKESTATIC, "Print", "doPrint", "(" + stringType + ")V", false);

    mainMethod.visitIincInsn(2, 1);
    mainMethod.visitJumpInsn(GOTO, loop);

    mainMethod.visitLabel(end);

    mainMethod.visitInsn(RETURN);
    mainMethod.visitMaxs(0, 0);
    mainMethod.visitEnd();

    // end main method

    // private static void doPrint(String s)
    MethodVisitor doPrintMethod = cw.visitMethod(ACC_PRIVATE + ACC_STATIC, "doPrint", "(" + stringType + ")V", null, null );


    doPrintMethod.visitFieldInsn(GETSTATIC, Type.getInternalName(java.lang.System.class), "out", PrintStream.class.descriptorString());
    doPrintMethod.visitIntInsn(ALOAD, 0);
    doPrintMethod.visitMethodInsn(INVOKEVIRTUAL, Type.getInternalName(PrintStream.class), "println", "(" + stringType + ")V", false);

    doPrintMethod.visitInsn(RETURN);

    doPrintMethod.visitMaxs(0, 0);
    doPrintMethod.visitEnd();

    //end doPrint

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

