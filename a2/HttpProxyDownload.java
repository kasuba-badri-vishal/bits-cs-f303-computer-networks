/* BeginGroupMembers */
/* f20170034@hyderabad.bits-pilani.ac.in S Rohith */
/* f20170270@hyderabad.bits-pilani.ac.in Kasuba Badri Vishal */
/* f20170025@hyderabad.bits-pilani.ac.in Raj Kashyap Mallala */
/* f20170209@hyderabad.bits-pilani.ac.in T Naga Sai Bharath */
/* EndGroupMembers */

import java.net.*;
import java.io.*;
import java.util.regex.*;
import java.util.Base64;
import javax.net.ssl.*;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import javax.net.ssl.X509TrustManager;

class HttpProxyDownload{
	static String website, hostAddr, username, passwd,  filename, webpage;
	static int port;

	private final static String base64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

    public static void main(String args[]) throws Exception{ 
        website  = (args.length==0)? "www.google.com"   : args[0];
        hostAddr = (args.length<=1)? "172.16.108.14"    : args[1];
        port        = (args.length<=2)? 3128               : Integer.parseInt(args[2]);
        username = (args.length<=3)? "csf303"           : args[3];
        passwd   = (args.length<=4)? "csf303"           : args[4];
        webpage  = (args.length<=5)? "index.html"       : args[5];
        filename = (args.length<=6)? "logo.png"         : args[6];
        int c;
        System.setProperty("https.protocols","TLSv1.2");

        // String encodedCred = Base64.getEncoder().encodeToString((username + ":" + passwd).getBytes("utf-8"));
        String encodedCred = encode(username + ":" + passwd);
        System.out.println(encodedCred);

        Socket s = new Socket(hostAddr, port);

        BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
        PrintStream out = new PrintStream(s.getOutputStream());
        
        String str = "CONNECT " + website + ":443 HTTP/1.1\r\nHost: " + website + "\r\nProxy-Connection: keep-alive\r\nProxy-Authorization: Basic " + encodedCred + "\r\n";
		out.println(str);

		BufferedReader in1 = new BufferedReader(new InputStreamReader(s.getInputStream()));;
        PrintStream out1 = new PrintStream(s.getOutputStream());

        String line;
		String doc = "";
		int flag = 0;
        while( (line=in.readLine()) != null ) {
            System.out.println( line );
            if(Pattern.matches(".*200 Connection established.*", line)){
				SSLContext sslContext = SSLContext.getInstance("TLS");
				TrustManager[] trustAll = new TrustManager[] {new TrustAllCertificates()};
				sslContext.init(null, trustAll, new java.security.SecureRandom());
				SSLSocketFactory ssf = (SSLSocketFactory) sslContext.getSocketFactory();
				SSLSocket sslSocket = (SSLSocket)ssf.createSocket(s, hostAddr,port,false);
				// SSLSocket sslSocket = (SSLSocket)ssf.createSocket(s, website,443,false);
				
				System.out.println("Starting Handshake");

                sslSocket.startHandshake();

				in1 = new BufferedReader(new InputStreamReader(sslSocket.getInputStream()));
				out1 = new PrintStream(sslSocket.getOutputStream());
                System.out.println("Handshake finished");

				String url = getImageURL(sslSocket, in1, out1);
				System.out.println(url);
				downloadImage(sslSocket, out1, url);

				break;
            }
        }
		// System.out.println(doc.length());
        in.close();
        out.close();
        s.close();
    }


	public static void downloadImage(SSLSocket socket, PrintStream out, String url) throws IOException{
		InputStream in = socket.getInputStream();
		int len = url.length();
		String file_name =  "";
		String file_type =  "";
		int j = url.length()-1;
		for(; url.charAt(j)!='.' && j>0; j--){
			file_type = url.charAt(j) + file_type;
		}
		for(j--; (url.charAt(j)!='/') && (url.charAt(j)!='\\') && j>0; j--){
			file_name = url.charAt(j) + file_name;
		}

		// OutputStream fout = new FileOutputStream(file_name + "." + file_type);
		OutputStream fout = new FileOutputStream(filename);

		if(!url.contains("www.") && (url.charAt(0)!='/' || url.charAt(0)!='\\')){
			url = "/" + url;
		}
		System.out.println(file_name + "   " + file_type);

		out.println("GET " + url + " HTTP/1.1\r\nHost: " + website + "\r\n\r\n");

		System.out.println("Downloading image...");
		
		int count;
		byte[] buffer = new byte[2048];
		boolean startDownload = false;
		boolean chunked = false;
		boolean flag = true;
		int m = 0;

		long start = 0;
		long end;
		outer:while(((count = in.read(buffer)) != -1)){
			if(startDownload){
				System.out.println(new String(buffer, 0, count));
				fout.write(buffer, 0, count);
				if(file_type.contains("GIF") && new String(buffer, 0, count).contains(";")) break outer;
				if(new String(buffer, 0, count).contains("END")) break outer;
			}else{
				String s = new String(buffer, 0, count);
				// System.out.println(s);
				if(s.contains("chunked")) chunked = true;
				if(chunked){
					for(int i=0; i<count-6 ; i++){
						if(buffer[i]=='P' && buffer[i+1]=='N' && buffer[i+2]=='G'){
							System.out.println(new String(buffer, i-1, count-i+1));
							fout.write(buffer, i-1, count-i+1);
							startDownload = true;
							break;
						}
					}
				}else{
					for(int i=0; i<count-6; i++){
						if(buffer[i]=='\r' && buffer[i+1]=='\n' && buffer[i+2]=='\r' && buffer[i+3]=='\n'){
							System.out.println(new String(buffer, i+4, count-i-4));
							fout.write(buffer, i+4, count-i-4);
							startDownload = true;
							break;
						}
					}

				}
			}
		}

		// outer:while((count = in.read(buffer)) != -1){
		// 		System.out.println(new String(buffer, 0, count));
		// 	if(startDownload){
		// 		fout.write(buffer, 0, count);
		// 		for(int i=0; i<count-2; i++){
		// 			if(buffer[i]=='E' && buffer[i+1]=='N' && buffer[i+2]=='D'){
		// 				break outer;	
		// 			}
		// 		}
		// 	}else{
		// 		for(int i=0; i<count-2; i++){
		// 			// if(buffer[i]==(byte)'\r' && buffer[i+1]==(byte)'\n' && buffer[i+2]==(byte)'\r' && buffer[i+3]==(byte)'\n'){
		// 			// if(buffer[i]==(byte)'P' && buffer[i+1]==(byte)'N' && buffer[i+2]==(byte)'G'){
		// 			if(buffer[i]==file_type.charAt(0) && buffer[i+1]==file_type.charAt(1) && buffer[i+2]==file_type.charAt(2)){		
		// 				startDownload = true;
		// 				fout.write(buffer, i-1, count-i+1);
		// 				break;
		// 			}
		// 		}
		// 	}
		// }
		System.out.println("Finished downloading.");

		in.close();
		fout.close();
		out.close();
	}

	public static String getImageURL(SSLSocket socket, BufferedReader in, PrintStream out) throws IOException{
		out.println("GET / HTTP/1.1\r\nHost: " + website + "\r\n\r\n");
		String line;
		String doc = "";
		boolean start = false;
		boolean chunked = false;
		boolean flag = false;
		while((line = in.readLine()) != null){
			if(line.contains("chunked")) chunked=true;
			if(start){
				if(chunked){
					if(flag){
						if(isHexNumber(line)) continue;
						doc+=line;
						doc+="\r\n";
					}else  flag=true;
				}else{
					doc+=line;
					doc+="\r\n";
				}

			}else{
				if(line.length()==0) start=true;
			}

            if(Pattern.matches(".*</html>.*", line)) break;
		}

		FileWriter writer = new FileWriter(webpage, false);
		writer.write(doc);
		writer.close();
		// while((line = in.readLine()) != null){
		// 	if(line.contains("chunked")) chunked=true;
		// 	if(start){
		// 		if(chunked){
		// 			if(flag){
		// 				doc+=line;
		// 			}else  flag=true;
		// 		}else{
		// 			doc+=line;
		// 		}
		// 	}else{
		// 		if(line.length()==0) start=true;
		// 	}

        //     if(line.contains("</html>")) break;
		// }

		byte b[] = doc.getBytes();
		System.out.print( new String(b, 0, b.length-1));

		// String body = "";
		// for(int i=0; i<b.length-4; i++){
		// 	if(b[i]=='\r' && b[i+1]=='\n' && b[i+2]=='\r' && b[i+3]=='\n'){
		// 	// if((b[i]=='<' && b[i+1]=='!' && (b[i+2]=='d' || b[i+2]=='D') && (b[i+2]=='o' || b[i+2]=='O'))){
		// 		body = new String(b, i+4, b.length-i-5);
		// 		// body += doc.substring(i, doc.length()-1);
		// 		break;
		// 	}
		// }


		Pattern p = Pattern.compile("src=\"(.*?)\"");
		Matcher m = p.matcher(doc);

		String url = "";

		// if (m.find()) {
		while (m.find()) {
			if(m.group(1).contains("logo")){
				url = m.group(1);
			}
		}
		// System.out.println(doc.length());
		return url;
	}

	public static String encode(String s) {

		// the result/encoded string, the padding string, and the pad count
		String r = "", p = "";
		int c = s.length() % 3;

		// add a right zero pad to make this string a multiple of 3 characters
		if (c > 0) {
			for (; c < 3; c++) {
				p += "=";
				s += "\0";
			}
		}

		// increment over the length of the string, three characters at a time
		for (c = 0; c < s.length(); c += 3) {

			// we add newlines after every 76 output characters, according to
			// the MIME specs
			if (c > 0 && (c / 3 * 4) % 76 == 0)
			r += "\r\n";

			// these three 8-bit (ASCII) characters become one 24-bit number
			int n = (s.charAt(c) << 16) + (s.charAt(c + 1) << 8)
				+ (s.charAt(c + 2));

			// this 24-bit number gets separated into four 6-bit numbers
			int n1 = (n >> 18) & 63, n2 = (n >> 12) & 63, n3 = (n >> 6) & 63, n4 = n & 63;

			// those four 6-bit numbers are used as indices into the base64
			// character list
			r += "" + base64chars.charAt(n1) + base64chars.charAt(n2)
				+ base64chars.charAt(n3) + base64chars.charAt(n4);
		}
		return r.substring(0, r.length() - p.length()) + p;
	}


	private static boolean isHexNumber (String cadena) {
		try {
			Long.parseLong(cadena, 16);
			return true;
		}
		catch (NumberFormatException ex) {
			// Error handling code...
			return false;
		}
	}
	
}


class TrustAllCertificates implements X509TrustManager {
	public void checkClientTrusted(X509Certificate[] certs, String authType) {
	}
	public void checkServerTrusted(X509Certificate[] certs, String authType) {
	}
	public X509Certificate[] getAcceptedIssuers() {
		return null;
	}
}