import java.util.Arrays;

/**
 * 
 */

/**
 * @author aishu
 *
 */
public class myAppTester {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
					int[] nw = new int[5];
			System.out.println("Original array");
			display(nw);
			System.out.println("After filling");
			Arrays.fill(nw, 8);
			display(nw);
			System.out.println("After changing value");
			nw[3]= 5;
			nw[1]=6;
			display(nw);
			System.out.println("After sorting");
			Arrays.sort(nw,1,4);
			display(nw);
			
		}
	
		public static void display(int [] a)
		{
			for (int i = 0; i < a.length; i++) {
				System.out.print(a[i] + " ");
				
				
			}System.out.println();
	}

}
