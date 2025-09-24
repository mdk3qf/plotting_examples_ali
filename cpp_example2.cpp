#include "TApplication.h"
#include "TROOT.h"
#include "TH2F.h"
#include "TF2.h"
#include "TF1.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TRandom3.h"

using namespace std;
using namespace ROOT::Math;

void cpp_2d_example(int samples=10000){
  gStyle->SetOptStat(0);  // turn off default stats box in histograms

  auto tr = new TRandom3();
  tr->SetSeed(0);  //uses current time as seed
  gRandom = tr;

  // A multi panel plot
  auto tc2 = new TCanvas("c2","C++",1200,800);
  tc2->Divide(2,2);
  tc2->cd(1); 
  
  // 2D Histogram filled with a 2D normal distribution
  auto hist1 = new TH2F("hist1","Random 2D gauss;x;y",100,50,150,100,50,150);

  // try out with inputs instead
  auto fpeak = new TF2("fpeak2","exp(-0.5*(x-[0])*(x-[0])/[1]/[1]) * exp(-0.5*(y-[2])*(y-[2])/[3]/[3])",50,150,50,150);
  fpeak->SetParameters(100,6,100,6);
  hist1->FillRandom("fpeak2",samples);
  hist1->Draw("colz");

  // add a random uniform offset to the 2D histogram
  auto hist2 = (TH2F*) hist1->Clone("hist2");
  hist2->SetTitle("2D Gauss+uniform offset;x;y");
  
  for (int i=0; i<samples/3; ++i){
    
    double x_uniform = tr->Uniform(50,150);
    double y_uniform = tr->Uniform(50,150);
    
    hist2->Fill(x_uniform, y_uniform);
  }
  
  tc2->cd(2);
  hist2->Draw("colz");


  // apply 1/x^2 offsets in each axis
  auto hist3 = (TH2F*) hist1->Clone("hist3");
  hist3->SetTitle("2D Gauss+1/x^2, 1/y^2 offset;x;y");
  auto base_x = new TF1("base_x","1/x/x",1,10);
  
  for (int i=0; i<samples*30; ++i){
    
    double x = base_x->GetRandom()*10+40;
    double y = base_x->GetRandom()*10+40;
    
    hist3->Fill(x, y);
  }
  tc2->cd(3)->SetLogz();
  hist3->Draw("colz");


  // a double gaussian, same mean but std_dev1 = 6, std_dev2 = 20
  auto hist4 = (TH2F*) hist1->Clone("hist4");
  hist4->SetTitle("Double 2D Gaussian;x;y");
  new TF2("double_gauss_2d",
    "(exp(-0.5*(x-100)*(x-100)/36) + exp(-0.5*(x-100)*(x-100)/400)) * (exp(-0.5*(y-100)*(y-100)/36) + exp(-0.5*(y-100)*(y-100)/400))",
    50, 150, 50, 150);
  
  hist4->FillRandom("double_gauss_2d",samples/2);
  
  tc2->cd(4);
  hist4->Draw("colz");
  tc2->Update();

  tc2->SaveAs("canvas2d_cpp.png");
  
}

int main(int argc, char **argv) {
  int nsamples=10000;  // set sample sizes

  TApplication theApp("App", &argc, argv);

  if (argc>1) nsamples=atoi(argv[1]);
  
  cpp_2d_example(nsamples);

  // view graphics in ROOT if we are in an interactive session
  if (!gROOT->IsBatch()) {
      cout << "To exit, quit ROOT from the File menu of the plot (or use control-C)" << endl;
    theApp.SetIdleTimer(30,".q"); // set up a failsafe timer to end the program
    theApp.Run(true);
  }
  return 0;
}