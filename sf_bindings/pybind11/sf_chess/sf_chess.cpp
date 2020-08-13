#include <pybind11/pybind11.h>
#include <iostream>
#include "stockfish/movegen.h"
#include "stockfish/thread.h"
#include "stockfish/position.h"
#include "stockfish/uci.h"
#include "stockfish/evaluate.h"


namespace py = pybind11;
const char* start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";

namespace PSQT {
    void init();
}

void init_stockfish() {
    UCI::init(Options);
    PSQT::init();
    Bitboards::init();
    Position::init();
    Bitbases::init();
    Search::init();
    Threads.set(Options["Threads"]);
    Search::clear(); // After threads are up
}


class SFPosition {
public:
    SFPosition(const std::string& fen) : thread_(Threads.main()) {
        states_ = StateListPtr(new std::deque<StateInfo>(1)); // Drop old and create a new one
        position_.init();
        position_.set(fen, false, &states_->back(), thread_.get());

    }
    SFPosition() : SFPosition(start_fen) {}

    std::string fen() {
        return position_.fen();
    }

    py::list legal_moves() {
        py::list moves;
        for (const ExtMove& move : MoveList<LEGAL>(position_)) {
            moves.append(UCI::move(move, 0));
        }
        return moves;
    }

private:
    std::unique_ptr<Thread> thread_;
    StateListPtr states_;
    Position position_;
};


PYBIND11_MODULE(sf_chess, m) {
    m.doc() = R"pbdoc(
        Stockfish wrapper.
    )pbdoc";

    py::class_<SFPosition>(m, "SFPosition")
        .def(py::init<const std::string&>())
		.def("fen", &SFPosition::fen)
        .def("legal_moves", &SFPosition::legal_moves)
        ;

    m.def("_init", &init_stockfish, R"pbdoc(Init
    )pbdoc");
}
