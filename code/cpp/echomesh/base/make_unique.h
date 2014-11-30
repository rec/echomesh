#pragma once

#include <memory>

// emulate variadics for 5 args
template<class T>
std::unique_ptr<T> make_unique(){
    return std::unique_ptr<T>(new T());
}

template<class T, class A0>
std::unique_ptr<T> make_unique(A0&& a0){
    return std::unique_ptr<T>(new T(std::forward<A0>(a0)));
}

template<class T, class A0, class A1>
std::unique_ptr<T> make_unique(A0&& a0, A1&& a1){
    return std::unique_ptr<T>(new T(std::forward<A0>(a0),
                                    std::forward<A1>(a1)));
}

template<class T, class A0, class A1, class A2>
std::unique_ptr<T> make_unique(A0&& a0, A1&& a1, A2&& a2){
    return std::unique_ptr<T>(new T(std::forward<A0>(a0),
                                    std::forward<A1>(a1), std::forward<A2>(a2)));
}

template<class T, class A0, class A1, class A2, class A3>
std::unique_ptr<T> make_unique(A0&& a0, A1&& a1, A2&& a2, A3&& a3){
    return std::unique_ptr<T>(new T(std::forward<A0>(a0),
                                    std::forward<A1>(a1), std::forward<A2>(a2),
                                    std::forward<A3>(a3)));
}

template<class T, class A0, class A1, class A2, class A3, class A4>
std::unique_ptr<T> make_unique(A0&& a0, A1&& a1, A2&& a2, A3&& a3, A4&& a4){
    return std::unique_ptr<T>(new T(std::forward<A0>(a0),
                                    std::forward<A1>(a1), std::forward<A2>(a2),
                                    std::forward<A3>(a3), std::forward<A4>(a4)));
}

