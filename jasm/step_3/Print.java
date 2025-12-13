class Print {

  public static void main(String[] args) {
    int max = 3;
    for (int i=0; i< max; i++) {
      doPrint("Print Count: " + i);
    }
  }

  private static void doPrint(String stringToPrint) {
    System.out.println(stringToPrint);
  }
}
