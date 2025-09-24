import ROOT as r
import sys

def python_2d_example(samples=10000):
    # 2D Histogram filled with normal distributions
    tr = r.TRandom3(12345)
    r.gRandom = tr # use tr as global generator
    
    hist1 = r.TH2F("hist2.1","Random 2D gauss;x;y",100,50,150,100,50,150)
    fpeak = r.TF2("fpeak2","exp(-0.5*(x-[0])*(x-[0])/[1]/[1]) * exp(-0.5*(y-[2])*(y-[2])/[3]/[3])",50,150,50,150)
    fpeak.SetParameters(100, 6, 100, 6)
    
    hist1.FillRandom("fpeak2", samples)
    tc1 = r.TCanvas("c1","Canvas1")
    hist1.Draw("colz")
    tc1.Update()

    # A multi panel plot
    tc2 = r.TCanvas("c2","Canvas2", 1200, 800)
    tc2.Divide(2,2) 
    tc2.cd(1)
    hist1.Draw("colz")

    # add a random uniform offset to the 2D histogram
    hist2 = hist1.Clone("hist2.2")
    hist2.SetTitle("2D Gauss+uniform offset;x;y")
    for i in range(samples//3):
        x_uniform = tr.Uniform(50, 150)
        y_uniform = tr.Uniform(50, 150)
        hist2.Fill(x_uniform, y_uniform)
    tc2.cd(2)
    hist2.Draw("colz")

    # apply independent 1/x^2 and 1/y^2 baselines
    hist3 = hist1.Clone("hist2.3")
    hist3.SetTitle("2D Gauss+1/x^2 offset;x;y")
    base_x = r.TF1("base_x","1/x/x", 1, 10)
    for i in range(samples*30):
        x = base_x.GetRandom()*10+40
        y = base_x.GetRandom()*10+40  
        hist3.Fill(x, y)
    tc2.cd(3).SetLogz()
    hist3.Draw("colz")

    # a double gaussian, same mean but std_dev1 = 6, std_dev2 = 20
    hist4 = hist1.Clone("hist2.4")
    hist4.SetTitle("Double 2D Gaussian;x;y")
    
    double_gauss_2d = r.TF2("double_gauss_2d", 
        "(exp(-0.5*(x-100)*(x-100)/36) + exp(-0.5*(x-100)*(x-100)/400)) * (exp(-0.5*(y-100)*(y-100)/36) + exp(-0.5*(y-100)*(y-100)/400))",
        50, 150, 50, 150)
    
    hist4.FillRandom("double_gauss_2d", samples//2)
    tc2.cd(4)
    hist4.Draw("colz")

    hist1.SetStats(0)
    hist2.SetStats(0)
    hist3.SetStats(0)
    hist4.SetStats(0)

    tc2.Update()
    input("hit 'return' to continue")
    
    tc2.SaveAs("canvas2d_py.png")
    

    
if __name__ == '__main__':
    samples=10000
    if len(sys.argv)>1: samples=int(sys.argv[1])
    python_2d_example(samples)